"""Initial scheduling schema

Revision ID: 1e814e5b0151
Revises: 
Create Date: 2025-06-15 14:04:26.938845

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1e814e5b0151'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")

    op.create_table('instructors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table('students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table('appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=False),
        sa.Column('appointment_time', postgresql.TSTZRANGE(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        postgresql.ExcludeConstraint((sa.column('instructor_id'), '='), (sa.column('appointment_time'), '&&'), using='gist', name='exclude_instructor_appointments_overlap'),
        postgresql.ExcludeConstraint((sa.column('student_id'), '='), (sa.column('appointment_time'), '&&'), using='gist', name='exclude_student_appointments_overlap'),
        sa.CheckConstraint('lower(appointment_time) < upper(appointment_time)', name='check_appointment_time_valid_range'),
        sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('instructor_availability',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=False),
        sa.Column('available_time', postgresql.TSTZRANGE(), nullable=False),
        postgresql.ExcludeConstraint((sa.column('instructor_id'), '='), (sa.column('available_time'), '&&'), using='gist', name='exclude_instructor_availability_overlaps'),
        sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('instructor_availability')
    op.drop_table('appointments')
    op.drop_table('students')
    op.drop_table('instructors')
