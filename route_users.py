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
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete, UserIn, UserInDB, UserDetail, UserWithUserDetailCreate, UserDetailRead, UserDetailCreate, UserChild, UserChildCreate, UserChildRead
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



# # create: user without details
# @router.post("/users", response_model=UserRead, tags=["User"])
# def create_user(user_in: UserIn):
#     with Session(engine) as session:
#         db_user = create_db_user(user_in)
#         session.add(db_user)
#         session.commit()
#         session.refresh(db_user)
#         return db_user



# create: user with user_details
@router.post("/users/signup", response_model=UserRead, tags=["User"])
def create_user_with_details(user_in: UserWithUserDetailCreate):
    with Session(engine) as session:
        username = user_in.username
        existing_user = session.exec(select(User).where(User.username == username)).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The username already exists")
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




# create: my user children
@router.post("/my/children", tags=["User"])
def create_my_user_children(children: list[UserChildCreate], current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        for child in children:
            child = UserChild.model_validate(child)
            user.user_children.append(child)
        session.add(user)
        session.commit()
        session.refresh(user)
        for child in user.user_children:
            child.user_id = user.id
        session.add(user)
        session.commit()
        session.refresh(user)
        return children



# delete: my user children
@router.delete("/my/children{child_id}", tags=["User"])
def delete_my_user_children(child_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Require login")
        child = session.exec(select(UserChild).where(UserChild.id == child_id and UserChild.user_id == user.id)).first()
        if child is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        session.delete(child)
        session.commit()
        return {"removed": "done"}




# read list
@router.get("/users", response_model=list[UserRead], tags=["User"])
def read_users_list(*, offset: int = 0, limit: int = Query(default=100, le=100), current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        if current_user.username != "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        # if not users:
        #     raise HTTPException(status_code=404, detail="Not found") # rather than this it should return empty list if no users
        return users



# read one
@router.get("/user/{username}", response_model=UserRead, tags=["User"])
def read_user(session: Annotated[Session, Depends(get_session)], username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return user



# read user with user details
@router.get("/users/details/{username}", response_model=UserDetailRead, tags=["User"])
def read_user_details(username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        if current_user.username != "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        user_details = user.user_details
        user_details_dict = user_details.model_dump()
        user_details_dict["username"] = user.username
        return user_details_dict



# patch: username and password -> require edit to get_hashed_password
@router.patch("/users/{username}", response_model=UserRead, tags=["User"])
def update_user(session: Annotated[Session, Depends(get_session)], username: str, user_update: UserUpdate, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    # db_user = session.get(User, user_id)
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise HTTPException(status_code=404, detail="Not found")
    user_update_dict = user_update.model_dump(exclude_unset=True) # pydantic型をdict型に変換してNULLなデータを除外する
    if user_update.plain_password:
        hashed_password = get_hashed_password(user_update.plain_password)
        user_update_dict.pop("plain_password")
        user_update_dict["hashed_password"] = hashed_password
    for key, value in user_update_dict.items():
        setattr(user, key, value) # user_dataのkey, valueをdb_userに割り当てる => 送られてきたuser_updateでNULLでないデータだけを上書きする
    session.add(user)
    session.commit()
    session.refresh(user)
    return user



# patch: user details
@router.patch("/userdetails/{username}", tags=["User"], response_model=UserDetailRead)
def patch_userdetails(username: str, new_user_details: UserDetailCreate, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        if username != current_user.username and current_user.username != "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == username)).one()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_details = user.user_details
        proper_new_user_details = new_user_details.model_dump(exclude_unset=True)
        for key, value in proper_new_user_details.items():
            setattr(user_details, key, value)
        session.add(user)
        session.commit()
        session.refresh(user_details)
        user_details_out = user_details.model_dump()
        user_details_out["username"] = username
        return user_details_out



# delete: user with details
@router.delete("/users/delete/{username}", tags=["User"])
def delete_user(username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        if current_user.username != username and current_user.username != "user":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == username)).one()
        if user is None:
            raise HTTPException(status_code=404, detail="Not found")
        user_details = session.exec(select(UserDetail).where(UserDetail.user_id == user.id)).one()
        session.delete(user)
        session.delete(user_details)
        session.commit()
        return {"deleted": user.username}





# return username
@router.get("/my/username", tags=["User"])
def get_username(current_user: Annotated[User, Depends(get_current_active_user)]):
    username = current_user.username
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return username




# json: get my user details
@router.get("/json/my/userdetails", tags=["User"], response_model=UserDetailRead)
def json_get_my_userdetails(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        user_details = session.exec(select(UserDetail).where(UserDetail.user_id == user.id)).one()
        user_details_dict = user_details.model_dump() # dict型に変更
        user_details_dict["username"] = current_user.username
        return user_details_dict



# json: get my user children
@router.get("/json/my/children", tags=["User"], response_model=list[UserChildRead])
def json_get_my_children(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        children = session.exec(select(UserChild).where(UserChild.user_id == user.id)).all()
        return children



# display user details
@router.get("/my/userdetails", tags=["User"], response_class=HTMLResponse)
def display_my_personal_info(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse("my/userdetails.html", context)



# children signup page
@router.get("/my/childrensignup", tags=["User"], response_class=HTMLResponse)
def display_children_signup_page(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("my/childrensignup.html", context)



# admin only: display: users
@router.get("/admin/users", tags=["User"], response_class=HTMLResponse)
def display_users(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("admin/users.html", context)


@router.get("/json/admin/users", tags=["User"])
def get_user_list_json(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user.username != "user":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        return {"response": "ok"}

