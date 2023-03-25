"""add companies competencies

Revision ID: 390f186e54dc
Revises: 85a35803a864
Create Date: 2023-03-25 23:26:47.167113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '390f186e54dc'
down_revision = '85a35803a864'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies_competencies',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('competency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['competency_id'], ['competencies.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'competency_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('companies_competencies')
    # ### end Alembic commands ###
