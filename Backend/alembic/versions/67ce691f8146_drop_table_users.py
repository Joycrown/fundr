"""Drop table users

Revision ID: 67ce691f8146
Revises: cb046ac59a36
Create Date: 2023-06-25 00:00:12.539835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67ce691f8146'
down_revision = 'cb046ac59a36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('requests')
    op.drop_table('payouts')
    op.drop_table('Cryptochil')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
