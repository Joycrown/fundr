"""create tables

Revision ID: 97d19929b08b
Revises: db357f48dd3c
Create Date: 2023-06-24 23:22:15.874873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d19929b08b'
down_revision = 'db357f48dd3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
