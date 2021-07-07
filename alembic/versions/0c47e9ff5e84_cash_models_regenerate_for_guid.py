"""Cash Models Regenerate for GUID

Revision ID: 0c47e9ff5e84
Revises: f45bbfddfabe
Create Date: 2021-07-07 06:15:18.110683

"""
from alembic import op
import sqlalchemy as sa
import app.models._guid

# revision identifiers, used by Alembic.
revision = '0c47e9ff5e84'
down_revision = 'f45bbfddfabe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cash',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cash_id'), 'cash', ['id'], unique=False)
    op.create_table('cash_deposit',
    sa.Column('id', app.models._guid.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('deposit_amount', sa.Integer(), nullable=False),
    sa.Column('request_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('ack_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_cancel', sa.Boolean(), nullable=True),
    sa.Column('cash_id', sa.Integer(), nullable=False),
    sa.Column('payment_key', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['cash_id'], ['cash.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cash_deposit_request_at'), 'cash_deposit', ['request_at'], unique=False)
    op.create_table('cash_usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('usage_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('usage_amount', sa.Integer(), nullable=False),
    sa.Column('cash_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cash_id'], ['cash.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cash_usage_id'), 'cash_usage', ['id'], unique=False)
    op.create_index(op.f('ix_cash_usage_usage_at'), 'cash_usage', ['usage_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cash_usage_usage_at'), table_name='cash_usage')
    op.drop_index(op.f('ix_cash_usage_id'), table_name='cash_usage')
    op.drop_table('cash_usage')
    op.drop_index(op.f('ix_cash_deposit_request_at'), table_name='cash_deposit')
    op.drop_table('cash_deposit')
    op.drop_index(op.f('ix_cash_id'), table_name='cash')
    op.drop_table('cash')
    # ### end Alembic commands ###
