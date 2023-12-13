from sqlalchemy import Integer, ForeignKey, Table, String, Column, MetaData, TIMESTAMP, JSON
from src.auth.model import user

metadata = MetaData()

group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("date_create", TIMESTAMP),
    Column("emails", JSON, nullable=False),
    Column("owner_id", Integer, ForeignKey(user.c.id))
)