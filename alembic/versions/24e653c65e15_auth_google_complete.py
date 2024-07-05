"""auth google complete

Revision ID: 24e653c65e15
Revises: e8b5499e065e
Create Date: 2024-07-05 03:25:23.842661

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '24e653c65e15'
down_revision: Union[str, None] = 'e8b5499e065e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_logout', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'last_logout')
    # ### end Alembic commands ###