from fastapi import FastAPI
import uvicorn
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from type_subscription.router import router as router_sub
from group.router import router as router_group

app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_sub)
app.include_router(router_group)

