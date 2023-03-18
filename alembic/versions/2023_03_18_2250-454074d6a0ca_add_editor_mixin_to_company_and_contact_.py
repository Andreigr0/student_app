"""add editor mixin to company and contact model

Revision ID: 454074d6a0ca
Revises: 94b4b6948210
Create Date: 2023-03-18 22:50:19.730604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '454074d6a0ca'
down_revision = '94b4b6948210'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('companies', sa.Column('updater_id', sa.Integer(), nullable=True))
    op.create_foreign_key('companies_updater_id', 'companies', 'users', ['updater_id'], ['id'])
    op.create_foreign_key('companies_creator_id', 'companies', 'users', ['creator_id'], ['id'])
    op.add_column('contacts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False))
    op.add_column('contacts', sa.Column('updated_at', sa.TIMESTAMP(), nullable=False))
    op.add_column('contacts', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('contacts', sa.Column('updater_id', sa.Integer(), nullable=True))
    op.create_foreign_key('contacts_updater_id', 'contacts', 'users', ['updater_id'], ['id'])
    op.create_foreign_key('contacts_creator_id', 'contacts', 'users', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('contacts_updater_id', 'contacts', type_='foreignkey')
    op.drop_constraint('contacts_creator_id', 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'updater_id')
    op.drop_column('contacts', 'creator_id')
    op.drop_column('contacts', 'updated_at')
    op.drop_column('contacts', 'created_at')
    op.drop_constraint('companies_updater_id', 'companies', type_='foreignkey')
    op.drop_constraint('companies_creator_id', 'companies', type_='foreignkey')
    op.drop_column('companies', 'updater_id')
    op.drop_column('companies', 'creator_id')
    # ### end Alembic commands ###