"""insert_user_trigger

Revision ID: d3483978a039
Revises: 44c5a5d34952
Create Date: 2025-07-11 00:19:25.820934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3483978a039'
down_revision: Union[str, None] = '44c5a5d34952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE FUNCTION insert_user_permissions_if_user()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.role = 'USER' THEN
            INSERT INTO user_permissions (id, broker_account_id, user_id, can_trade, created_at, updated_at)
            SELECT
                gen_random_uuid(),
                bsa.id,
                NEW.id,
                FALSE,
                now(),
                now()
            FROM broker_service_accounts bsa
            WHERE bsa.broker_id = NEW.ref_id;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_insert_user_permissions
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION insert_user_permissions_if_user();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_insert_user_permissions ON users;")
    op.execute("DROP FUNCTION IF EXISTS insert_user_permissions_if_user;")
