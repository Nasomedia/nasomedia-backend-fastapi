"""empty message

Revision ID: c2d3676191f3
Revises: 
Create Date: 2021-03-24 08:34:41.370822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d3676191f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('thumbnail', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_series_description'), 'series', ['description'], unique=False)
    op.create_index(op.f('ix_series_id'), 'series', ['id'], unique=False)
    op.create_index(op.f('ix_series_title'), 'series', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('episode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('episode_order', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('series_id', sa.Integer(), nullable=False),
    sa.Column('thumbnail', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_episode_episode_order'), 'episode', ['episode_order'], unique=False)
    op.create_index(op.f('ix_episode_id'), 'episode', ['id'], unique=False)
    op.create_table('episode_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_order', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('episode_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['episode_id'], ['episode.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_episode_image_id'), 'episode_image', ['id'], unique=False)
    op.create_index(op.f('ix_episode_image_image_order'), 'episode_image', ['image_order'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_episode_image_image_order'), table_name='episode_image')
    op.drop_index(op.f('ix_episode_image_id'), table_name='episode_image')
    op.drop_table('episode_image')
    op.drop_index(op.f('ix_episode_id'), table_name='episode')
    op.drop_index(op.f('ix_episode_episode_order'), table_name='episode')
    op.drop_table('episode')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_series_title'), table_name='series')
    op.drop_index(op.f('ix_series_id'), table_name='series')
    op.drop_index(op.f('ix_series_description'), table_name='series')
    op.drop_table('series')
    # ### end Alembic commands ###
