# --- route_users.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated

# my modules
from database import engine, get_session
from models.items import Item, ItemCreate, ItemRead, ItemUpdate, ItemDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete, UserIn, UserInDB, UserDetail, UserWithUserDetailCreate, UserDetailRead
from route_auth import get_hashed_password
from route_auth import get_current_active_user

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# database session
# session = Session(engine)

# routes below 000000000000000000000000000000000000


# create User model from UserIn model converting plain password into hashed password
def create_db_user(user_in: UserIn):
    hashed_password = get_hashed_password(user_in.plain_password)
    db_user = User(**user_in.model_dump(), hashed_password=hashed_password)
    # db_user = User(**user_in.dict(), hashed_password=hashed_password) # dict() => model_dump()
    return db_user



# create
@router.post("/users", response_model=UserRead, tags=["User"])
def create_user(user_in: UserIn):
    with Session(engine) as session:
        db_user = create_db_user(user_in)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user



# create
@router.post("/users/signup", response_model=UserRead, tags=["User"])
def create_user_with_details(user_in: UserWithUserDetailCreate):
    with Session(engine) as session:
        db_user = create_db_user(user_in)
        db_user_details = create_db_user_details(user_in)
        db_user.user_details = db_user_details
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        db_user.user_details.user_id = db_user.id
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user



# create user with details converting plain password into hashed password
def create_db_user_with_details(user_in: UserWithUserDetailCreate):
    hashed_password = get_hashed_password(user_in.plain_password)
    db_user = User(**user_in.model_dump(), hashed_password=hashed_password)
    return db_user

# return user details
def create_db_user_details(user_in: UserWithUserDetailCreate):
    db_user_details = UserDetail(**user_in.model_dump())
    return db_user_details




# read list
@router.get("/users", response_model=list[UserRead], tags=["User"])
def read_users_list(*, offset: int = 0, limit: int = Query(default=100, le=100), current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        if current_user.username != "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        # if not users:
        #     raise HTTPException(status_code=404, detail="Not found") # should return empty list if no users
        return users



# read one
@router.get("/user/{username}", response_model=UserRead, tags=["User"])
def read_user(session: Annotated[Session, Depends(get_session)], username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return user



# read user with user details
@router.get("/users/details/{username}", response_model=UserDetailRead, tags=["User"])
def read_user_details(username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        if current_user.username != username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user_details = user.user_details
        return user_details



# patch
@router.patch("/users/{username}", response_model=UserRead, tags=["User"])
def update_user(session: Annotated[Session, Depends(get_session)], username: str, user_update: UserUpdate, current_user: Annotated[User, Depends(get_current_active_user)]):
    # db_user = session.get(User, user_id)
    db_user = session.exec(select(User).where(User.username == username)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Not found")
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    user_data = user_update.model_dump(exclude_unset=True) # pydanticのuser_update型でNULLなデータを除外する
    for key, value in user_data.items():
        setattr(db_user, key, value) # user_dataのkey, valueをdb_userに割り当てる => 送られてきたuser_updateでNULLでないデータだけを上書きする
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user



# delete
@router.delete("/users/delete/{username}", tags=["User"])
def delete_user(username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        if current_user.username != username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Not found")
        user_details = session.exec(select(UserDetail).where(UserDetail.user_id == user.id)).first()
        session.delete(user)
        session.delete(user_details)
        session.commit()
        return {"deleted": user.username}



