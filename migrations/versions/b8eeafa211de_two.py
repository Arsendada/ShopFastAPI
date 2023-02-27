"""two

Revision ID: b8eeafa211de
Revises: 17a4ca6cce31
Create Date: 2023-02-27 21:49:16.829462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8eeafa211de'
down_revision = '17a4ca6cce31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_username_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    # ### end Alembic commands ###
