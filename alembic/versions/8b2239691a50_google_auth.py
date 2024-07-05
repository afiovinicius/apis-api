"""google auth

Revision ID: 8b2239691a50
Revises: f54e28257d79
Create Date: 2024-06-30 00:42:07.572202

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b2239691a50"
down_revision: Union[str, None] = "f54e28257d79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "is_provider_auth", sa.String(), nullable=False, server_default="email"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_provider_auth")
    # ### end Alembic commands ###