"""empty message

Revision ID: 73b9255b0757
Revises: 
Create Date: 2019-04-15 14:33:28.430659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73b9255b0757'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=64), nullable=True),
    sa.Column('paper_name', sa.Text(), nullable=True),
    sa.Column('author_email', sa.String(length=120), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('visibility', sa.Boolean(), nullable=False),
    sa.Column('tool_name', sa.String(length=200), nullable=True),
    sa.Column('link_to_pdf', sa.String(length=250), nullable=True),
    sa.Column('link_to_archive', sa.String(length=250), nullable=True),
    sa.Column('link_to_tool_webpage', sa.String(length=250), nullable=True),
    sa.Column('link_to_demo', sa.String(length=250), nullable=True),
    sa.Column('bibtex', sa.Text(), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=False),
    sa.Column('download_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tagname', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_tagname'), 'tags', ['tagname'], unique=True)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commenter_email', sa.String(length=120), nullable=True),
    sa.Column('commenter_name', sa.String(length=120), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('upvoted', sa.Boolean(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=80), nullable=True),
    sa.Column('fileurl', sa.String(length=200), nullable=True),
    sa.Column('filetype', sa.String(length=50), nullable=True),
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_filename'), 'files', ['filename'], unique=False)
    op.create_index(op.f('ix_files_fileurl'), 'files', ['fileurl'], unique=False)
    op.create_table('paper_to_tags',
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paper_to_tags')
    op.drop_index(op.f('ix_files_fileurl'), table_name='files')
    op.drop_index(op.f('ix_files_filename'), table_name='files')
    op.drop_table('files')
    op.drop_table('comments')
    op.drop_index(op.f('ix_tags_tagname'), table_name='tags')
    op.drop_table('tags')
    op.drop_table('papers')
    # ### end Alembic commands ###