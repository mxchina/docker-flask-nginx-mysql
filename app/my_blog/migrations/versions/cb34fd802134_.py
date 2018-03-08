"""empty message

Revision ID: cb34fd802134
Revises: 7234b82da91d
Create Date: 2017-11-07 03:04:39.129681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb34fd802134'
down_revision = '7234b82da91d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload_image', sa.Column('image_md5', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('upload_image', 'image_md5')
    # ### end Alembic commands ###