# --- route_users.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated

# my modules
from database import engine, get_session
from models.items import Item, ItemCreate, ItemRead, ItemUpdate, ItemDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete, UserIn, UserInDB
from route_auth import get_hashed_password

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# database session
session = Session(engine)

# routes below 000000000000000000000000000000000000


# create User model from UserIn model converting plain password into hashed password
def create_db_user(user_in: UserIn):
    hashed_password = get_hashed_password(user_in.plain_password)
    db_user = User(**user_in.model_dump(), hashed_password=hashed_password)
    # db_user = User(**user_in.dict(), hashed_password=hashed_password) # dict() => model_dump()
    return db_user



# create
@router.post("/users", response_model=UserRead, tags=["User"])
async def create_user(user_in: UserIn):
    with session:
        db_user = create_db_user(user_in)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user



# read list
@router.get("/users", response_model=list[UserRead], tags=["User"])
def read_users_list(offset: int = 0, limit: int = Query(default=100, le=100)):
    with session:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        # if not users:
        #     raise HTTPException(status_code=404, detail="Not found")
        return users




# read one
@router.get("/user/{user_id}", response_model=UserRead, tags=["User"])
def read_user(session: Annotated[Session, Depends(get_session)], user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user



# update
@router.patch("/users/{user_id}", response_model=UserRead, tags=["User"])
def update_user(session: Annotated[Session, Depends(get_session)], user_id: int, user_update: UserUpdate):
    db_user = session.get(User, user_id)
    # db_user = session.select(User).where(User.id == user_id) # same as above
    if not db_user:
        raise HTTPException(status_code=404, detail="Not found")
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value) # 空欄を省いてpydantic型(dict型)にしたuser_update = user_dataのkey, valueをdb_userに割り当てる
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user



# delete
@router.delete("/users/{user_id}", tags=["User"])
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(user)
    session.commit()
    return {"deleted": user}


