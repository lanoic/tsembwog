from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass  # Run: alembic revision --autogenerate -m "init" && alembic upgrade head

def downgrade():
    pass
