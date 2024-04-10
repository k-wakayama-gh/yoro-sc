# --- route_lessons.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated
from datetime import datetime, timedelta, timezone

# my modules
from database import engine, get_session
from models.lessons import Lesson, LessonCreate, LessonRead, LessonUpdate, LessonDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete
from route_auth import get_current_active_user

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# database session
# session = Session(engine)

# common query parameters
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, offset: int = 0, limit: int = Query(default=100, le=100)):
        self.q = q
        self.offset = offset
        self.limit = limit

# routes below 000000000000000000000000000000000000

# lesson application start date and time
test_start_time = datetime(year=2024, month=4, day=9, hour=22, minute=30, second=0, tzinfo=timezone(timedelta(hours=9)))

start_time = datetime(year=2024, month=4, day=10, hour=7, minute=0, second=0, tzinfo=timezone(timedelta(hours=9)))

# def: return current time
# def current_time():
#     current_time = datetime.now()
#     return current_time


# create
@router.post("/lessons", response_model=LessonRead, tags=["Lesson"])
def create_lesson(lesson_create: LessonCreate):
    with Session(engine) as session:
        db_lesson = Lesson.model_validate(lesson_create)
        session.add(db_lesson)
        session.commit()
        session.refresh(db_lesson)
        return db_lesson



# display lessons sync
@router.get("/jinja/lessons", response_class=HTMLResponse, tags=["html"], response_model=list[LessonRead])
def display_lessons_sync(session: Annotated[Session, Depends(get_session)], commons: Annotated[CommonQueryParams, Depends()], request: Request):
    lessons = session.exec(select(Lesson).offset(commons.offset).limit(commons.limit)).all() # Lesson here must be a database model i.e. table: not LessonRead model
    # if not lessons:
    #     raise HTTPException(status_code=404, detail="Not found")
    context = {
        "request": request,
        "lessons": lessons,
        "title": "教室一覧",
    }
    return templates.TemplateResponse("lessons.html", context) # this context includes lesson.id even if it is not loaded in the html corresponding response_model




# display lessons async
@router.get("/lessons", response_class=HTMLResponse, tags=["Lesson"], response_model=list[LessonRead])
def display_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("lessons.html", context)




# json: get lesson list
@router.get("/json/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_lesson_list_json(query: Annotated[CommonQueryParams, Depends()]):
    current_time = (datetime.utcnow() + timedelta(hours=9)).replace(tzinfo=timezone(timedelta(hours=9)))
    if current_time < start_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="lesson signup is not allowed yet")
    with Session(engine) as session:
        lessons = session.exec(select(Lesson).offset(query.offset).limit(query.limit)).all()
        return lessons




# json admin: get lesson list
@router.get("/json/admin/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_lesson_list_json(query: Annotated[CommonQueryParams, Depends()], current_user: Annotated[User, Depends(get_current_active_user)]):
    current_time = (datetime.utcnow() + timedelta(hours=9)).replace(tzinfo=timezone(timedelta(hours=9)))
    if current_time < test_start_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="lesson signup is not allowed yet")
    if not current_user.username == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not allowed to access")
    with Session(engine) as session:
        lessons = session.exec(select(Lesson).offset(query.offset).limit(query.limit)).all()
        return lessons




# read one
@router.get("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def read_lesson(session: Annotated[Session, Depends(get_session)], lesson_id: int):
    lesson = session.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Not found")
    return lesson



# update
@router.patch("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def update_lesson(lesson_id: int, lesson_update: LessonUpdate):
    with Session(engine) as session:
        db_lesson = session.get(Lesson, lesson_id)
        if not db_lesson:
            raise HTTPException(status_code=404, detail="Not found")
        
        lesson_data = lesson_update.model_dump(exclude_unset=True)
        
        for key, value in lesson_data.items():
            setattr(db_lesson, key, value)
            
        session.add(db_lesson)
        session.commit()
        session.refresh(db_lesson)
        return db_lesson



# delete
@router.delete("/lessons/{lesson_id}", tags=["Lesson"])
def delete_lesson(*, session: Session = Depends(get_session), lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not allowed")
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(lesson)
    session.commit()
    return {"deleted": lesson}




# read: my lessons
@router.get("/json/my/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        my_lessons = user.lessons
        return my_lessons



# post: sign up to a lessons with auth
@router.post("/lessons/{id}", response_model=list[LessonRead], tags=["Lesson"])
def create_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)], id: int):
    current_time = (datetime.utcnow() + timedelta(hours=9)).replace(tzinfo=timezone(timedelta(hours=9)))
    if current_time < start_time and current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="lesson signup is not allowed yet")
    with Session(engine) as session:
        new_lesson = session.exec(select(Lesson).where(Lesson.id == id)).first()
        if new_lesson.year != 2024 or new_lesson.season != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        if not new_lesson in user.lessons:
            user.lessons.append(new_lesson)
            session.add(user)
            session.commit()
            session.refresh(user)
        new_lesson.capacity_left = new_lesson.capacity - len(new_lesson.users)
        session.add(new_lesson)
        session.commit()
        session.refresh(new_lesson)
        my_lessons = user.lessons
        return my_lessons



# display my lessons async
@router.get("/my/lessons", response_class=HTMLResponse, tags=["Lesson"], response_model=list[LessonRead])
def display_my_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("my/lessons.html", context)



# display admin lessons async for management
@router.get("/admin/lessons", response_class=HTMLResponse, tags=["Lesson"], response_model=list[LessonRead])
def display_superuser_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("admin/lessons.html", context)



# cancel a lesson
@router.delete("/my/lessons/{lesson_id}", tags=["Lesson"])
def delete_my_lesson(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        cancel_lesson = session.get(Lesson, lesson_id)
        if not cancel_lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        if cancel_lesson.year != 2024 or cancel_lesson.season != 1:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Outdated")
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user in cancel_lesson.users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not signed up")
        user.lessons.remove(cancel_lesson)
        session.commit()
        cancel_lesson.capacity_left = cancel_lesson.capacity - len(cancel_lesson.users)
        session.add(cancel_lesson)
        session.commit()
        session.refresh(cancel_lesson)
        return {"removed": cancel_lesson}




# admin: read signuped user list for each lesson
@router.get("/json/admin/{lesson_id}/member", response_model=list[UserRead], tags={"Lesson"})
def admin_read_lesson_member_list(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
        lesson_member = lesson.users
        return lesson_member



# admin: delete: lesson member
@router.delete("/admin/{lesson_id}/remove/{username}", tags=["Lesson"])
def admin_remove_lesson_member(lesson_id: int, username: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
        lesson_title = lesson.title
        lesson_member = lesson.users
        user = session.exec(select(User).where(User.username == username)).one()
        user_details = (user.user_details).model_dump()
        user_fullname = user_details["last_name"] + "　" + user_details["first_name"]
        lesson_member.remove(user)
        session.add(lesson)
        session.commit()
        session.refresh(lesson)
        message = f"{username}：{user_fullname}を{lesson_title}から削除しました。"
        return {"removed done": message}



# read: lesson signup position
@router.get("/json/my/lessons/{lesson_id}/position", tags=["Lesson"])
def json_read_lesson_signup_position(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        lesson_member = lesson.users
        if not user in lesson_member:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not signed up to this lesson")
            user_position = 0
        else:
            user_position = lesson_member.index(user) + 1
        return user_position



# read: lesson signup position
@router.get("/json/my/lessons/position", tags=["Lesson"])
def json_read_lesson_signup_position_all(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        lessons = session.exec(select(Lesson).where(Lesson.year == 2024)).all()
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        position_list = []
        for lesson in lessons:
            lesson_member = lesson.users
            if not user in lesson_member:
                user_position = 0
            else:
                user_position = lesson_member.index(user) + 1
            positioon_dict = {"lesson_id": lesson.id, "user_position": user_position}
            position_list.append(positioon_dict)
        return position_list



@router.get("/json/admin/user/{user_id}/lessons", tags=["Lesson"])
def admin_json_read_user_lesson_list(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        user = session.get(User, user_id)
        user_lessons = user.lessons
        return user_lessons



# post: sign up to a lessons with auth
@router.post("/admin/user/{user_id}/lessons/{lesson_id}", response_model=list[LessonRead], tags=["Lesson"])
def create_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)], user_id: int, lesson_id: int):
    current_time = (datetime.utcnow() + timedelta(hours=9)).replace(tzinfo=timezone(timedelta(hours=9)))
    if current_time < start_time and current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="lesson signup is not allowed yet")
    with Session(engine) as session:
        new_lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
        # if new_lesson.year != 2024 or new_lesson.season != 1:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.id == user_id)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        if not new_lesson in user.lessons:
            user.lessons.append(new_lesson)
            session.add(user)
            session.commit()
            session.refresh(user)
        new_lesson.capacity_left = new_lesson.capacity - len(new_lesson.users)
        session.add(new_lesson)
        session.commit()
        session.refresh(new_lesson)
        user_lessons = user.lessons
        return user_lessons

