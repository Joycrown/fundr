"""auto users

Revision ID: 9a11e09f00d6
Revises: 29f37b3c7862
Create Date: 2022-10-25 00:16:29.013085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a11e09f00d6'
down_revision = '29f37b3c7862'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.add_column('users', sa.Column('country', sa.String(), nullable=False))
    op.add_column('users', sa.Column('phone_no', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('transaction_id', sa.String(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=' False ', nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['phone_no'])
    op.create_primary_key(None, 'users',['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'transaction_id')
    op.drop_column('users', 'password')
    op.drop_column('users', 'phone_no')
    op.drop_column('users', 'country')
    op.drop_column('users', 'email')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'id')
    # ### end Alembic commands ###
