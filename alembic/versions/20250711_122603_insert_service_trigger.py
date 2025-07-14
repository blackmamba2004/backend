"""insert_service_trigger

Revision ID: 7c75b52e0d67
Revises: d3483978a039
Create Date: 2025-07-11 12:26:03.532770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c75b52e0d67'
down_revision: Union[str, None] = 'd3483978a039'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE FUNCTION insert_user_permissions_if_broker_account()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO user_permissions (id, broker_account_id, user_id, can_trade, created_at, updated_at)
        SELECT
            gen_random_uuid(),
            NEW.id,
            u.id,
            FALSE,
            now(),
            now()
        FROM users u
        WHERE u.ref_id = NEW.broker_id AND role='USER';
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_insert_user_permissions_broker_account
    AFTER INSERT ON broker_service_accounts
    FOR EACH ROW
    EXECUTE FUNCTION insert_user_permissions_if_broker_account();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_insert_user_permissions_broker_account ON broker_service_accounts;")
    op.execute("DROP FUNCTION IF EXISTS insert_user_permissions_if_broker_account;")
