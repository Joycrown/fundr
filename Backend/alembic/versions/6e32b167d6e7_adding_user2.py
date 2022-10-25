"""adding user2

Revision ID: 6e32b167d6e7
Revises: f061f6437589
Create Date: 2022-10-25 01:42:28.714563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e32b167d6e7'
down_revision = 'f061f6437589'
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
