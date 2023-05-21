"""Drop table users

Revision ID: fbbb2c0fa931
Revises: d6e91ae6f464
Create Date: 2023-05-08 13:29:21.193490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbbb2c0fa931'
down_revision = 'd6e91ae6f464'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('requests')
    op.drop_table('payouts')
    op.drop_table('admin')
    op.drop_table('Cryptochil')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###