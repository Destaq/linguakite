"""empty message

Revision ID: 4ed27af5f1ca
Revises: 692df012a26b
Create Date: 2022-07-25 18:34:37.799022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed27af5f1ca'
down_revision = '692df012a26b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('lemma_rank', sa.Integer(), nullable=False))
    op.add_column('word', sa.Column('word_rank', sa.Integer(), nullable=True))
    op.drop_column('word', 'definition')
    op.drop_column('word', 'translation')
    op.drop_column('word', 'frequency')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('frequency', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('word', sa.Column('translation', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.add_column('word', sa.Column('definition', sa.VARCHAR(length=512), autoincrement=False, nullable=False))
    op.drop_column('word', 'word_rank')
    op.drop_column('word', 'lemma_rank')
    # ### end Alembic commands ###