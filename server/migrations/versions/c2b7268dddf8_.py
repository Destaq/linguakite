"""empty message

Revision ID: c2b7268dddf8
Revises: 5597e15cac8f
Create Date: 2022-07-26 19:04:41.133453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2b7268dddf8'
down_revision = '5597e15cac8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_tag_association',
    sa.Column('text_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['text_id'], ['text.id'], ),
    sa.PrimaryKeyConstraint('text_id', 'tag_id')
    )
    op.drop_table('text_tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_tag',
    sa.Column('text_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name='text_tag_tag_id_fkey'),
    sa.ForeignKeyConstraint(['text_id'], ['text.id'], name='text_tag_text_id_fkey'),
    sa.PrimaryKeyConstraint('text_id', 'tag_id', name='text_tag_pkey')
    )
    op.drop_table('text_tag_association')
    # ### end Alembic commands ###
