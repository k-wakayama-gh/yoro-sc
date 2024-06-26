"""first revision auto

Revision ID: 812fb31b777a
Revises: 
Create Date: 2024-03-18 04:23:15.591419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '812fb31b777a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("lesson", sa.Column("lessons", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('content', sa.VARCHAR(), nullable=True),
    sa.Column('is_done', sa.BOOLEAN(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lesson',
    sa.Column('year', sa.INTEGER(), nullable=False),
    sa.Column('season', sa.INTEGER(), nullable=False),
    sa.Column('number', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('teacher', sa.VARCHAR(), nullable=False),
    sa.Column('day', sa.VARCHAR(), nullable=False),
    sa.Column('time', sa.VARCHAR(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('capacity', sa.INTEGER(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('capacity_left', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('useruserdetaillink',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('user_details_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_details_id'], ['userdetail.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'user_details_id')
    )
    op.create_table('item',
    sa.Column('item_name', sa.VARCHAR(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userlessonlink',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('lesson_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'lesson_id')
    )
    op.create_table('usertodolink',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('todo_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'todo_id')
    )
    op.create_table('userdetail',
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(), nullable=False),
    sa.Column('last_name', sa.VARCHAR(), nullable=False),
    sa.Column('first_name_furigana', sa.VARCHAR(), nullable=False),
    sa.Column('last_name_furigana', sa.VARCHAR(), nullable=False),
    sa.Column('tel', sa.VARCHAR(), nullable=False),
    sa.Column('postal_code', sa.VARCHAR(), nullable=False),
    sa.Column('address', sa.VARCHAR(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('created_time', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.create_table(
    #     "userchild",
    #     sa.Column("id", sa.Integer, primary_key=True),
    #     sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
    #     sa.Column("child_first_name", sa.String),
    #     sa.Column("child_last_name", sa.String),
    #     sa.Column("child_first_name_furigana", sa.String),
    #     sa.Column("child_last_name_furigana", sa.String)
    # )
    # ### end Alembic commands ###
