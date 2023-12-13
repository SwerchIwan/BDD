import json

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.type_subscription.models import subscription


router = APIRouter(
    prefix="/sub",
    tags=["Subscription"]
)


@router.get("/")
async def get_subscription(session: AsyncSession = Depends(get_async_session)):
    query = select(subscription)
    result = await session.execute(query)
    subscriptions = result.fetchall()  # Получаем все строки результата запроса

    subscription_list = []
    for row in subscriptions:
        subscription_dict = {
            "id": row.id,
            "type": row.type,
            "advantages": row.advantages,
            "expiration": row.expiration,
            "price": str(row.price)
        }
        subscription_list.append(subscription_dict)

    return subscription_list
