"""add Note, Tag

Revision ID: 3bd25b84b1b3
Revises: e4f834f9ca67
Create Date: 2025-01-06 13:23:00.796568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bd25b84b1b3'
down_revision: Union[str, None] = 'e4f834f9ca67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
