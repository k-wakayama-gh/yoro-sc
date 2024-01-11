"""added sqlmodel models

Revision ID: aff1d7561b5a
Revises: e3f7058a0b5b
Create Date: 2024-01-10 22:38:22.131077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aff1d7561b5a'
down_revision: Union[str, None] = 'e3f7058a0b5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
