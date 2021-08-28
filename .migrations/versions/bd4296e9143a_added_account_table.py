"""Added account table

Revision ID: bd4296e9143a
Revises: 
Create Date: 2021-08-28 17:07:39.770071

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bd4296e9143a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sector',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sector_id'), 'sector', ['id'], unique=False)
    op.create_table('subsector',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subsector_id'), 'subsector', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=10), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('stock',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('symbol', sa.String(length=5), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.Column('sub_sector_id', sa.Integer(), nullable=True),
    sa.Column('listing_date', sa.Date(), server_default=sa.text('now()'), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['sector_id'], ['sector.id'], ),
    sa.ForeignKeyConstraint(['sub_sector_id'], ['subsector.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stock_id'), 'stock', ['id'], unique=False)
    op.create_index(op.f('ix_stock_symbol'), 'stock', ['symbol'], unique=True)
    op.create_table('trader',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('fname', sa.String(length=64), nullable=True),
    sa.Column('lname', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trader_id'), 'trader', ['id'], unique=False)
    op.create_table('offer',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('trader_id', sa.Integer(), nullable=True),
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('buy', sa.Boolean(), nullable=True),
    sa.Column('sell', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.ForeignKeyConstraint(['trader_id'], ['trader.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_offer_id'), 'offer', ['id'], unique=True)
    op.create_table('portfolio',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('trader_id', sa.Integer(), nullable=True),
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.ForeignKeyConstraint(['trader_id'], ['trader.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_id'), 'portfolio', ['id'], unique=False)
    op.create_table('pricehistory',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.Column('buy', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('sell', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pricehistory_id'), 'pricehistory', ['id'], unique=False)
    op.create_table('trade',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=3), nullable=True),
    sa.Column('offer_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['trader.id'], ),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['trader.id'], ),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trade_id'), 'trade', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trade_id'), table_name='trade')
    op.drop_table('trade')
    op.drop_index(op.f('ix_pricehistory_id'), table_name='pricehistory')
    op.drop_table('pricehistory')
    op.drop_index(op.f('ix_portfolio_id'), table_name='portfolio')
    op.drop_table('portfolio')
    op.drop_index(op.f('ix_offer_id'), table_name='offer')
    op.drop_table('offer')
    op.drop_index(op.f('ix_trader_id'), table_name='trader')
    op.drop_table('trader')
    op.drop_index(op.f('ix_stock_symbol'), table_name='stock')
    op.drop_index(op.f('ix_stock_id'), table_name='stock')
    op.drop_table('stock')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_subsector_id'), table_name='subsector')
    op.drop_table('subsector')
    op.drop_index(op.f('ix_sector_id'), table_name='sector')
    op.drop_table('sector')
    # ### end Alembic commands ###
