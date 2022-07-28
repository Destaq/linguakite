"""empty message

Revision ID: 5597e15cac8f
Revises: 384a620201b2
Create Date: 2022-07-26 18:48:36.415632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5597e15cac8f'
down_revision = '384a620201b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('lemmatized_content', sa.String(), nullable=False))
    op.drop_column('text', 'lemmatized_text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('lemmatized_text', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('text', 'lemmatized_content')
    # ### end Alembic commands ###