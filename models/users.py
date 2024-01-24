# --- models/users.py ---

# modules
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# my modules
from models import link_table

if TYPE_CHECKING:
    import lessons

# models below 000000000000000000000


# base model
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)



# includes hashed password: never send this out!!!!!
class UserInDB(UserBase):
    hashed_password: str



# table
class User(UserInDB, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    lessons: List["lessons.Lesson"] = Relationship(back_populates="users", link_model=link_table.UserLessonLink)



# create: this includes a plain password: never send this out!!!!!
class UserCreate(UserBase):
    plain_password: str
    pass



# read
class UserRead(UserBase):
    id: int



# update
class UserUpdate(UserBase):
    pass



# delete
class UserDelete(UserBase):
    pass


