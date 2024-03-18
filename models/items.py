# --- models/items.py ---

# modules
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# models below 000000000000000000000


# base model
class ItemBase(SQLModel):
    item_name: str
    price: int = Field(default=0)
    description: Optional[str] = Field(default=None)



# table
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



# create
class ItemCreate(ItemBase):
    pass



# read
class ItemRead(ItemBase):
    id: int



# update
class ItemUpdate(ItemBase):
    pass



# delete
class ItemDelete(ItemBase):
    pass


