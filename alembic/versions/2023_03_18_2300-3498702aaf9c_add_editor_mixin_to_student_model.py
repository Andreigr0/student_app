"""add editor mixin to student model

Revision ID: 3498702aaf9c
Revises: 454074d6a0ca
Create Date: 2023-03-18 23:00:36.946973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3498702aaf9c'
down_revision = '454074d6a0ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('students', sa.Column('updater_id', sa.Integer(), nullable=True))
    op.create_foreign_key('students_updater_id', 'students', 'users', ['updater_id'], ['id'])
    op.create_foreign_key('students_creator_id', 'students', 'users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('students_updater_id', 'students', type_='foreignkey')
    op.drop_constraint('students_creator_id', 'students', type_='foreignkey')
    op.drop_column('students', 'updater_id')
    op.drop_column('students', 'creator_id')
    # ### end Alembic commands ###
