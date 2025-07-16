"""Update user profile

Revision ID: 6ecb1e2c215d
Revises: 1a87a1170348
Create Date: 2025-07-10 09:38:32.511603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql


# revision identifiers, used by Alembic.
revision: str = '6ecb1e2c215d'
down_revision: Union[str, None] = '1a87a1170348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    gender_enum = psql.ENUM('male', 'female', 'other', name='user_gender')
    gender_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('User', sa.Column('birth_date', sa.Date(), nullable=True))
    op.add_column('User', sa.Column('gender', sa.Enum('male', 'female', 'other', name='user_gender'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('User', 'gender')
    op.drop_column('User', 'birth_date')

    gender_enum = psql.ENUM('male', 'female', 'other', name='user_gender')
    gender_enum.drop(op.get_bind(), checkfirst=True)
