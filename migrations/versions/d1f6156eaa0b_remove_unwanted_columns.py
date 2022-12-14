"""remove unwanted columns

Revision ID: d1f6156eaa0b
Revises: 0b9c6c8fef53
Create Date: 2022-08-04 14:20:06.485190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1f6156eaa0b'
down_revision = '0b9c6c8fef53'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
