# --- models/todos.py ---

# modules
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# models below 000000000000000000000


# base model
class TodoBase(SQLModel):
    title: str = Field(index=True)
    content: Optional[str] = Field(default=None, index=True)
    is_done: bool = Field(default=False) #is_done: bool = Noneにすると、patchでも空のリクエストがあるたびにboolの値をFalseにしようとする。Fieldを使うと最初だけFalseにしようとする。



# table
class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



# create
class TodoCreate(TodoBase):
    pass



# read
class TodoRead(TodoBase):
    id: int



# update
class TodoUpdate(TodoBase):
    title: Optional[str] = Field(default=None, index=True) # Field(default=None)はデータがない場合も適切に処理されるようになる。
    pass



# delete
class TodoDelete(TodoBase):
    pass


