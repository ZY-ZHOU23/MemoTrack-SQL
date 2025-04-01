"""change_metric_type_to_category

Revision ID: 211bfa03eb9f
Revises: 1f6c01f0e403
Create Date: 2025-03-31 19:41:06.361496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '211bfa03eb9f'
down_revision: Union[str, None] = '1f6c01f0e403'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new category column
    op.add_column('metrics', sa.Column('category', sa.String(length=100), nullable=True))
    
    # Migrate data from metric_type to category
    op.execute("""
        UPDATE metrics
        SET category = metric_type
    """)
    
    # Make category column not nullable
    op.alter_column('metrics', 'category', nullable=False)
    
    # Drop the old metric_type column
    op.drop_column('metrics', 'metric_type')


def downgrade() -> None:
    """Downgrade schema."""
    # Add metric_type column back
    op.add_column('metrics', sa.Column('metric_type', mysql.ENUM('financial', 'health', 'productivity', 'custom'), nullable=True))
    
    # Migrate data from category to metric_type
    op.execute("""
        UPDATE metrics
        SET metric_type = CASE 
            WHEN category IN ('financial', 'health', 'productivity') THEN category 
            ELSE 'custom' 
        END
    """)
    
    # Make metric_type column not nullable
    op.alter_column('metrics', 'metric_type', nullable=False)
    
    # Drop the category column
    op.drop_column('metrics', 'category')
