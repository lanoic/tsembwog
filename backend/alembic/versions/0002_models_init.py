from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_models_init'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True)
    )
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('role', sa.String(), server_default='member', nullable=False),
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True)
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('certificates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('uid', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('amount_mwh', sa.Float(), nullable=False),
        sa.Column('issue_date', sa.DateTime(), nullable=False),
        sa.Column('valid_until', sa.DateTime(), nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(), server_default='active', nullable=False)
    )

    op.create_table('dsr_devices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('site', sa.String(), nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('max_kw', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False)
    )

    op.create_table('dsr_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('target_reduction_kw', sa.Float(), nullable=False),
        sa.Column('note', sa.String(), server_default='', nullable=False)
    )

    op.create_table('dsr_event_registrations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), sa.ForeignKey('dsr_events.id'), nullable=False),
        sa.Column('device_id', sa.Integer(), sa.ForeignKey('dsr_devices.id'), nullable=False),
        sa.Column('committed_kw', sa.Float(), nullable=False),
        sa.UniqueConstraint('event_id','device_id', name='uix_event_device')
    )

    op.create_table('btm_devices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('site', sa.String(), nullable=False),
        sa.Column('storage_capacity_kwh', sa.Float(), nullable=False),
        sa.Column('current_soc', sa.Float(), server_default='0.5', nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table('btm_readings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('device_id', sa.Integer(), sa.ForeignKey('btm_devices.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('load_kw', sa.Float(), nullable=False),
        sa.Column('solar_kw', sa.Float(), nullable=False)
    )

    op.create_table('api_keys',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('label', sa.String(), server_default='default', nullable=False),
        sa.Column('owner_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

def downgrade():
    op.drop_table('api_keys')
    op.drop_table('btm_readings')
    op.drop_table('btm_devices')
    op.drop_table('dsr_event_registrations')
    op.drop_table('dsr_events')
    op.drop_table('dsr_devices')
    op.drop_table('certificates')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    op.drop_table('organizations')
