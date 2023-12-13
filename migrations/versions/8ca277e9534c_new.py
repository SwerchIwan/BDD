"""NEW

Revision ID: 8ca277e9534c
Revises: 3a75ec0676c2
Create Date: 2023-12-12 11:45:29.139024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ca277e9534c'
down_revision: Union[str, None] = '3a75ec0676c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
