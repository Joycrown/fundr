"""add payment to requests

Revision ID: 0809c8ee8ec0
Revises: e8c17057fea1
Create Date: 2023-02-11 16:28:25.554269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0809c8ee8ec0'
down_revision = 'e8c17057fea1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('password', sa.String(), server_default='N/A', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requests', 'password')
    # ### end Alembic commands ###
