"""create historias_clinicas table

Revision ID: 2bf812e45bae
Revises: 
Create Date: 2025-05-29 15:13:05.512960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '2bf812e45bae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pacientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('document_type', sa.String(), nullable=False),
    sa.Column('document_number', sa.String(), nullable=False),
    sa.Column('birth_date', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('blood_type', sa.String(), nullable=True),
    sa.Column('allergies', sa.String(), nullable=True),
    sa.Column('medical_history', sa.String(), nullable=True),
    sa.Column('insurance', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=True),
    sa.Column('referred_by', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document_number')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('full_name', sa.Text(), nullable=False),
    sa.Column('document_number', sa.Text(), nullable=False),
    sa.Column('birth_date', sa.String(length=20), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('eps', sa.String(length=50), nullable=True),
    sa.Column('blood_type', sa.String(length=5), nullable=True),
    sa.Column('allergies', sa.Text(), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('two_factor_enabled', sa.Boolean(), nullable=True),
    sa.Column('two_factor_code', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('reason', sa.String(length=255), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('historias_clinicas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('record_date', sa.Date(), nullable=True),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('blood_pressure', sa.String(), nullable=True),
    sa.Column('heart_rate', sa.Integer(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('oxygen_saturation', sa.Integer(), nullable=True),
    sa.Column('diagnosis', sa.String(), nullable=False),
    sa.Column('diagnosis_details', sa.Text(), nullable=True),
    sa.Column('treatment', sa.Text(), nullable=True),
    sa.Column('medications', sqlite.JSON(), nullable=True),
    sa.Column('observations', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('historias_clinicas')
    op.drop_table('appointment')
    op.drop_table('user')
    op.drop_table('pacientes')
    # ### end Alembic commands ###
