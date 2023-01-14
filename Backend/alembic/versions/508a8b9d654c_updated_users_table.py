"""updated users table

Revision ID: 508a8b9d654c
Revises: 05fbf686a840
Create Date: 2023-01-11 15:15:16.711566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '508a8b9d654c'
down_revision = '05fbf686a840'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('upgrading_reason', sa.String(), server_default='N/A', nullable=False))
    op.add_column('users', sa.Column('scaling_reason', sa.String(), server_default='N/A', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'scaling_reason')
    op.drop_column('users', 'upgrading_reason')
    # ### end Alembic commands ###
