"""make_category_id_nullable

Revision ID: 3f7c01f0e405
Revises: 211bfa03eb9f
Create Date: 2023-04-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f7c01f0e405'
down_revision = '211bfa03eb9f'
branch_labels = None
depends_on = None


def upgrade():
    # Make category_id nullable
    with op.batch_alter_table('entries', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=sa.Integer(),
               nullable=True)


def downgrade():
    # Make category_id non-nullable again
    with op.batch_alter_table('entries', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=sa.Integer(),
               nullable=False) 