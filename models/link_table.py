# --- models/link_table.py ---

# modules
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    import users, lessons

# models below

class UserLessonLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.id", primary_key=True)


