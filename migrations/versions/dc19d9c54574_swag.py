"""swag

Revision ID: dc19d9c54574
Revises: bd90940b43e8
Create Date: 2023-12-17 21:36:13.341304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc19d9c54574'
down_revision = 'bd90940b43e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('language', sa.String(), nullable=True))
        batch_op.create_unique_constraint(None, ['job_name'])
        batch_op.drop_column('args')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('args', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('language')
        batch_op.drop_column('job_name')

    # ### end Alembic commands ###
