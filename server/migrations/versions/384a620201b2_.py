"""empty message

Revision ID: 384a620201b2
Revises: ab0f924e8dfc
Create Date: 2022-07-26 18:40:13.321627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '384a620201b2'
down_revision = 'ab0f924e8dfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('content', sa.String(), nullable=False))
    op.drop_column('text', 'text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('text', 'content')
    # ### end Alembic commands ###
