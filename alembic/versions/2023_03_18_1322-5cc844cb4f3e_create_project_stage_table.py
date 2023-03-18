"""create project_stage table

Revision ID: 5cc844cb4f3e
Revises: 2a797d0cef2c
Create Date: 2023-03-18 13:22:47.103023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cc844cb4f3e'
down_revision = '2a797d0cef2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_stage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('finish_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_stage_id'), 'project_stage', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_stage_id'), table_name='project_stage')
    op.drop_table('project_stage')
    # ### end Alembic commands ###
