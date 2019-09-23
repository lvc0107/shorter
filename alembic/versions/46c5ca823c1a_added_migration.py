"""added migration

Revision ID: 46c5ca823c1a
Revises: 
Create Date: 2019-09-12 00:23:00.113984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "46c5ca823c1a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shorter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("usage_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_usage", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["code"], ["shorter.code"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stats")
    op.drop_table("shorter")
    # ### end Alembic commands ###