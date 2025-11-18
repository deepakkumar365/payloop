""""add_superadmin_enum"

Revision ID: 25f788404b20
Revises: 2b56bb559a85
Create Date: 2025-11-17 23:01:26.882181

"""
from alembic import op
import sqlalchemy as sa


revision = '25f788404b20'
down_revision = '2b56bb559a85'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE userrole ADD VALUE 'SUPERADMIN' BEFORE 'ADMIN'")


def downgrade() -> None:
    op.execute("ALTER TYPE userrole RENAME TO userrole_old")
    op.execute("CREATE TYPE userrole AS ENUM ('ADMIN', 'AGENT')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::text::userrole")
    op.execute("DROP TYPE userrole_old")
