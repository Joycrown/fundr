"""create users table

Revision ID: 29f37b3c7862
Revises: 
Create Date: 2022-10-24 04:29:43.821567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29f37b3c7862'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users'), sa.Column('id', sa.Integer(), nullable= False),
    sa.Column('id', sa.Integer(), nullable= False),
    sa.Column('first_name', sa.String(), nullable= False),
    sa.Column('last_name', sa.String(), nullable= False),
    sa.Column('email', sa.String(), nullable= False),
    sa.Column('country', sa.String(), nullable= False),
    sa.Column('phone_no', sa.String(), nullable= False),
    sa.Column('password', sa.String(), nullable= False),
    sa.Column('transaction_id', sa.String(), nullable= False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable= False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email','phone_no'),



def downgrade() -> None:
    op.drop_table('users')
  
