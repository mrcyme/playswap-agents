"""swag

Revision ID: 566c3ffa6efe
Revises: 0f5d2a6355de
Create Date: 2023-12-17 21:42:20.547386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566c3ffa6efe'
down_revision = '0f5d2a6355de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###
