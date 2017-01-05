"""empty message

Revision ID: e9da4f9c2397
Revises: b5b36637219d
Create Date: 2017-01-05 16:07:46.136755

"""

# revision identifiers, used by Alembic.
revision = 'e9da4f9c2397'
down_revision = 'b5b36637219d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('poster', sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'poster')
    # ### end Alembic commands ###