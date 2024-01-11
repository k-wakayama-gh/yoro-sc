# --- models/lessons.py ---

# modules
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# models below 000000000000000000000


# base model
class LessonBase(SQLModel):
    number: int
    title: str = Field(index=True)
    teacher: str = Field(index=True)
    day: Optional[str]
    time: Optional[str]
    price: Optional[int]
    description: Optional[str] =Field(default=None, index=True)




# table
class Lesson(LessonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



# create
class LessonCreate(LessonBase):
    pass



# read
class LessonRead(LessonBase):
    id: int



# update
class LessonUpdate(LessonBase):
    pass



# delete
class LessonDelete(LessonBase):
    pass


