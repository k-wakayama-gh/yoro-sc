# --- models/lessons.py ---

# modules
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# my modules
from models import link_table

if TYPE_CHECKING:
    import users

# models below 000000000000000000000


# base model
class LessonBase(SQLModel):
    year: int
    season: int
    number: int
    title: str
    teacher: str
    day: str
    time: str
    price: int
    description: Optional[str]



# table
class Lesson(LessonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    users: List["users.User"] = Relationship(back_populates="lessons", link_model=link_table.UserLessonLink)



# create
class LessonCreate(LessonBase):
    pass



# read or out
class LessonRead(LessonBase):
    id: int



# update: independent SQLModel model: Optional[...] = None works properly with Patch requests
class LessonUpdate(SQLModel):
    year: Optional[int] = None
    season: Optional[int] = None
    number: Optional[int] = None
    title: Optional[str] = None
    teacher: Optional[str] = None
    day: Optional[str] = None
    time: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None



# delete
class LessonDelete(LessonBase):
    pass


