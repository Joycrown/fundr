"""Drop table users

Revision ID: 9bc7f97b6acd
Revises: 9de0f34c472a
Create Date: 2023-05-25 11:19:46.222778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bc7f97b6acd'
down_revision = '9de0f34c472a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
