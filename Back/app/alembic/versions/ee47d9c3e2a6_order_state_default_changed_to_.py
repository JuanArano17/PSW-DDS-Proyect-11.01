"""order state default changed to confirmesd

Revision ID: ee47d9c3e2a6
Revises: 14686a9cb25f
Create Date: 2024-05-29 18:43:25.994099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee47d9c3e2a6'
down_revision: Union[str, None] = '14686a9cb25f'
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