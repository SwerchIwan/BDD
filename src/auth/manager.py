from typing import Optional, Union, Generator

from fastapi import Depends, Request, HTTPException, status

from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas, InvalidPasswordException
from fastapi_users.jwt import SecretType, decode_jwt, generate_jwt

from .model import User
from .utils import get_user_db
from random import randint

from config import SECRET_AUTH
from src.tasks.tasks import send_welcome_message
import passlib.pwd


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        code = randint(100000, 999999)
        send_welcome_message(user.username, user.email, code)
        print(f"User {user.id} has registered. ")

    async def request_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        """
        Start a verification request.

        Triggers the on_after_request_verify handler on success.

        :param user: The user to verify.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserInactive: The user is inactive.
        :raises UserAlreadyVerified: The user is already verified.
        """
        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        await self.on_after_request_verify(user, token, request)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        await self.user_db.update(user, {"is_active": True})
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(self, password: str, user: Union[schemas.UC, models.UP]) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1
        user_dict["is_verified"] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        await self.user_db.update(created_user,{"is_active": False})

        return created_user


async def get_user_manager(user_db: User = Depends(get_user_db)) -> Generator[UserManager, None, None]:
    yield UserManager(user_db)