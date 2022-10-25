"""adding user

Revision ID: f061f6437589
Revises: c903c590e83b
Create Date: 2022-10-25 01:28:32.596395

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f061f6437589'
down_revision = 'c903c590e83b'
branch_labels = None
depends_on = None


def upgrade() -> None:
   op.create_table('users',
   sa.Column('id',sa.Integer(),nullable=False, primary_key=True),
   sa.Column('first_name',sa.String(),nullable=False),
   sa.Column('last_name',sa.String(),nullable=False),
   sa.Column('email',sa.String(),nullable=False, unique=True),
   sa.Column('phone_no',sa.Integer(),nullable=False,unique=True),
   sa.Column('country',sa.String(),nullable=False),
   sa.Column('transaction_id',sa.String(),nullable=False),
   sa.Column('password',sa.String(),nullable=False),
   sa.Column('is_admin', sa.Boolean(), server_default=' False ', nullable=True),
   sa.Column('created_at',  sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
   )

def downgrade() -> None:
    op.drop_table('users')
