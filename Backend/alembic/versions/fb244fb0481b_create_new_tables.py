"""Create new tables

Revision ID: fb244fb0481b
Revises: cedf737c08c5
Create Date: 2023-05-25 22:27:41.727918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb244fb0481b'
down_revision = 'cedf737c08c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_no', sa.Numeric(), nullable=False),
    sa.Column('role', sa.String(), server_default='Trader', nullable=False),
    sa.Column('capital', sa.String(), nullable=False),
    sa.Column('status', sa.String(), server_default='Received', nullable=False),
    sa.Column('reason', sa.String(), server_default='N/A', nullable=False),
    sa.Column('phase', sa.String(), server_default='Evaluation', nullable=False),
    sa.Column('upgrade_to', sa.String(), server_default='N/A', nullable=False),
    sa.Column('scale_to', sa.String(), server_default='N/A', nullable=False),
    sa.Column('mt_login', sa.String(), server_default='N/A', nullable=False),
    sa.Column('metatrader_password', sa.String(), server_default='N/A', nullable=False),
    sa.Column('mt_server', sa.String(), server_default='N/A', nullable=False),
    sa.Column('analytics', sa.String(), server_default='N/A', nullable=False),
    sa.Column('status_upgrade', sa.String(), server_default='N/A', nullable=False),
    sa.Column('status_scale', sa.String(), server_default='N/A', nullable=False),
    sa.Column('status_payout', sa.String(), server_default='N/A', nullable=False),
    sa.Column('upgrading_reason', sa.String(), server_default='N/A', nullable=False),
    sa.Column('scaling_reason', sa.String(), server_default='N/A', nullable=False),
    sa.Column('account_id_meta', sa.String(), server_default='N/A', nullable=False),
    sa.Column('transaction_id', sa.String(), nullable=False),
    sa.Column('transaction_link', sa.String(), nullable=False),
    sa.Column('type_meta', sa.String(), server_default='N/A', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('phone_no'),
    sa.UniqueConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
