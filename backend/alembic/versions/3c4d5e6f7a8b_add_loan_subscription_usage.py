"""Add loan, subscription, and usage-based billing models

Revision ID: 3c4d5e6f7a8b
Revises: 25f788404b20
Create Date: 2025-11-17 23:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '3c4d5e6f7a8b'
down_revision = '25f788404b20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE paymenttype AS ENUM ('LOAN', 'SUBSCRIPTION', 'USAGE_BASED')")
    op.add_column('customers', sa.Column('payment_type', sa.Enum('LOAN', 'SUBSCRIPTION', 'USAGE_BASED', name='paymenttype'), nullable=True))
    
    op.create_table('loans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('principal_amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('interest_rate', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('total_repayable_amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('repayment_frequency', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', name='loanrepaymentfrequency'), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_loans_id'), 'loans', ['id'], unique=False)
    
    op.create_table('loan_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loan_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('pending_balance', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=False),
    sa.Column('payment_mode', sa.String(), nullable=True),
    sa.Column('recorded_by_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['loan_id'], ['loans.id'], ),
    sa.ForeignKeyConstraint(['recorded_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_loan_payments_id'), 'loan_payments', ['id'], unique=False)
    
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('subscription_amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('billing_cycle', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', name='billingcycle'), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_id'), 'subscriptions', ['id'], unique=False)
    
    op.create_table('bills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('bill_number', sa.String(), nullable=False),
    sa.Column('billing_period_start', sa.DateTime(), nullable=False),
    sa.Column('billing_period_end', sa.DateTime(), nullable=False),
    sa.Column('amount_due', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('previous_pending_balance', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('total_amount_to_collect', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'PARTIALLY_PAID', 'FULLY_PAID', name='billstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bill_number')
    )
    op.create_index(op.f('ix_bills_id'), 'bills', ['id'], unique=False)
    
    op.create_table('bill_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bill_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=False),
    sa.Column('payment_mode', sa.String(), nullable=True),
    sa.Column('recorded_by_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['recorded_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bill_payments_id'), 'bill_payments', ['id'], unique=False)
    
    op.create_table('usage_based_billings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(), nullable=False),
    sa.Column('rate_per_unit', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('rate_type', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usage_based_billings_id'), 'usage_based_billings', ['id'], unique=False)
    
    op.create_table('usage_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usage_billing_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('usage_date', sa.Date(), nullable=False),
    sa.Column('quantity_used', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['usage_billing_id'], ['usage_based_billings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usage_records_id'), 'usage_records', ['id'], unique=False)
    
    op.create_table('usage_bills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usage_billing_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('bill_number', sa.String(), nullable=False),
    sa.Column('billing_period_start', sa.Date(), nullable=False),
    sa.Column('billing_period_end', sa.Date(), nullable=False),
    sa.Column('total_usage_days', sa.Integer(), nullable=False),
    sa.Column('total_quantity_used', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('rate_per_unit', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('amount_due', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('previous_pending_balance', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('total_amount_to_collect', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'PARTIALLY_PAID', 'FULLY_PAID', name='usagebillingstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['usage_billing_id'], ['usage_based_billings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bill_number')
    )
    op.create_index(op.f('ix_usage_bills_id'), 'usage_bills', ['id'], unique=False)
    
    op.create_table('usage_bill_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usage_bill_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=False),
    sa.Column('payment_mode', sa.String(), nullable=True),
    sa.Column('recorded_by_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['recorded_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['usage_bill_id'], ['usage_bills.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usage_bill_payments_id'), 'usage_bill_payments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_usage_bill_payments_id'), table_name='usage_bill_payments')
    op.drop_table('usage_bill_payments')
    op.drop_index(op.f('ix_usage_bills_id'), table_name='usage_bills')
    op.drop_table('usage_bills')
    op.drop_index(op.f('ix_usage_records_id'), table_name='usage_records')
    op.drop_table('usage_records')
    op.drop_index(op.f('ix_usage_based_billings_id'), table_name='usage_based_billings')
    op.drop_table('usage_based_billings')
    op.drop_index(op.f('ix_bill_payments_id'), table_name='bill_payments')
    op.drop_table('bill_payments')
    op.drop_index(op.f('ix_bills_id'), table_name='bills')
    op.drop_table('bills')
    op.drop_index(op.f('ix_subscriptions_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_loan_payments_id'), table_name='loan_payments')
    op.drop_table('loan_payments')
    op.drop_index(op.f('ix_loans_id'), table_name='loans')
    op.drop_table('loans')
    op.drop_column('customers', 'payment_type')
    op.execute("DROP TYPE paymenttype")
