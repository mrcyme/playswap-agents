"""change to active.

Revision ID: fe568c285b42
Revises: 5bdd62c6c82c
Create Date: 2023-12-17 17:25:37.951648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe568c285b42'
down_revision = '5bdd62c6c82c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=True))
        batch_op.drop_column('publish')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publish', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('active')

    # ### end Alembic commands ###