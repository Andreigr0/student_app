"""add project_roles table

Revision ID: 0b35aa085d6c
Revises: b11a819482be
Create Date: 2023-03-19 16:33:31.605057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b35aa085d6c'
down_revision = 'b11a819482be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('work_format', sa.Enum('FullDay', 'RemoteWork', 'Flexible', name='projectroleworkformatenum'), nullable=False),
    sa.Column('workload', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_roles_id'), 'project_roles', ['id'], unique=False)
    op.create_table('project_role_need_competency',
    sa.Column('project_role_id', sa.Integer(), nullable=False),
    sa.Column('competency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], ),
    sa.ForeignKeyConstraint(['project_role_id'], ['project_roles.id'], ),
    sa.PrimaryKeyConstraint('project_role_id', 'competency_id')
    )
    op.create_table('project_role_will_competency',
    sa.Column('project_role_id', sa.Integer(), nullable=True),
    sa.Column('competency_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], ),
    sa.ForeignKeyConstraint(['project_role_id'], ['project_roles.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_role_will_competency')
    op.drop_table('project_role_need_competency')
    op.drop_index(op.f('ix_project_roles_id'), table_name='project_roles')
    op.drop_table('project_roles')
    sa.Enum(name='projectroleworkformatenum').drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###