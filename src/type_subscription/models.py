from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey, JSON, DECIMAL

from src.auth.model import user

metadata = MetaData()

subscription = Table(
    "subscription",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False),
    Column("advantages", JSON, nullable=False),
    Column("expiration", Integer, nullable=False),
    Column("price", DECIMAL, nullable=False),
)


subscription_user = Table(
    "subscription_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", TIMESTAMP, nullable=False),
    Column("sub_id", Integer, ForeignKey(subscription.c.id)),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)

