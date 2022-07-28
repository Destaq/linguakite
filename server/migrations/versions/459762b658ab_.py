"""empty message

Revision ID: 459762b658ab
Revises: 1710bc2632c3
Create Date: 2022-07-28 23:14:05.754575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459762b658ab'
down_revision = '1710bc2632c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('difficulty', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('text', 'difficulty')
    # ### end Alembic commands ###