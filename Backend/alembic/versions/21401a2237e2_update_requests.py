"""update requests

Revision ID: 21401a2237e2
Revises: 17e4c61d01b0
Create Date: 2023-01-09 23:21:08.162153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21401a2237e2'
down_revision = '17e4c61d01b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('phone_no', sa.Numeric(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('account_purchased', sa.String(), nullable=False),
    sa.Column('time_stamp', sa.String(), nullable=False),
    sa.Column('transaction_id', sa.String(), nullable=False),
    sa.Column('transaction_link', sa.String(), nullable=False),
    sa.Column('status_payment', sa.String(), server_default='N/A', nullable=False),
    sa.Column('status_upgrade', sa.String(), server_default='N/A', nullable=False),
    sa.Column('status_scale', sa.String(), server_default='N/A', nullable=False),
    sa.Column('current_phase', sa.String(), server_default='N/A', nullable=False),
    sa.Column('upgrade_to', sa.String(), server_default='N/A', nullable=False),
    sa.Column('current_capital', sa.String(), server_default='N/A', nullable=False),
    sa.Column('scale_to', sa.String(), server_default='N/A', nullable=False),
    sa.Column('analytics_upgrade', sa.String(), server_default='N/A', nullable=False),
    sa.Column('analytics_scale', sa.String(), server_default='N/A', nullable=False),
    sa.Column('type', sa.String(), server_default='Payment', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_no')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    # ### end Alembic commands ###
