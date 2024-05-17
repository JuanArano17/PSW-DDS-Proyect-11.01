"""add state column for orders

Revision ID: 2f4220a451e1
Revises: 8acad48495a4
Create Date: 2024-05-18 00:05:28.939608

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f4220a451e1"
down_revision: Union[str, None] = "8acad48495a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "Order",
        sa.Column(
            "state",
            sa.Enum(
                "PENDING",
                "CONFIRMED",
                "CANCELLED",
                "SHIPPED",
                "DELIVERED",
                name="orderstate",
            ),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("Order", "state")
    # ### end Alembic commands ###