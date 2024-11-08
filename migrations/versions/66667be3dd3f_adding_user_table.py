"""Adding User Table

Revision ID: 66667be3dd3f
Revises: 8dc8f9c5e997
Create Date: 2024-10-15 18:01:13.440855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66667be3dd3f'
down_revision = '8dc8f9c5e997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login_attempts', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('is_locked', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_locked')
        batch_op.drop_column('login_attempts')

    # ### end Alembic commands ###
