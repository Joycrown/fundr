"""Drop table users

Revision ID: 3591fe924b38
Revises: 028915641d17
Create Date: 2023-05-21 23:26:41.029709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3591fe924b38'
down_revision = '028915641d17'
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