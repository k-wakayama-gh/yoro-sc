# --- route_lessons.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated

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
session = Session(engine)

# common query parameters
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, offset: int = 0, limit: int = Query(default=100, le=100)):
        self.q = q
        self.offset = offset
        self.limit = limit

# routes below 000000000000000000000000000000000000


# create
@router.post("/lessons", response_model=LessonRead, tags=["Lesson"])
def create_lesson(lesson_create: LessonCreate):
    with session:
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
@router.get("/lessons", response_class=HTMLResponse, tags=["html"], response_model=list[LessonRead])
def display_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("lessons.html", context)




# read list as json
@router.get("/json/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_lesson_list_json(query: Annotated[CommonQueryParams, Depends()]):
    with session:
        lessons = session.exec(select(Lesson).offset(query.offset).limit(query.limit)).all()
        return lessons




# read one
@router.get("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def read_lesson(session: Annotated[Session, Depends(get_session)], lesson_id: int):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Not found")
    return lesson



# update
@router.patch("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def update_lesson(lesson_id: int, lesson_update: LessonUpdate):
    with session:
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
def delete_lesson(*, session: Session = Depends(get_session), lesson_id: int):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(lesson)
    session.commit()
    return {"deleted": lesson}




# read: my lessons
@router.get("/json/my/lessons", response_model=list[LessonRead])
def read_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)]):
    with session:
        user = session.exec(select(User).where(User.username == current_user.username)).first()
        my_lessons = user.lessons
        return my_lessons



# create: sign up to a lessons with auth
@router.post("/lessons/{id}", response_model=list[LessonRead])
def create_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)], id: int):
    with session:
        new_lesson = session.exec(select(Lesson).where(Lesson.id == id)).first()
        if new_lesson.year != 2024 or new_lesson.season != 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == current_user.username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        if not new_lesson in user.lessons:
            user.lessons.append(new_lesson)
            session.add(user)
            session.commit()
            session.refresh(user)
        my_lessons = user.lessons
        return my_lessons



# display my lessons async
@router.get("/my/lessons", response_class=HTMLResponse, tags=["html"], response_model=list[LessonRead])
def display_my_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("my/lessons.html", context)



# display superuser lessons async for management
@router.get("/superuser/lessons", response_class=HTMLResponse, tags=["html"], response_model=list[LessonRead])
def display_superuser_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("superuser/lessons.html", context)



# cancel a lesson
@router.delete("/my/lessons/{lesson_id}", tags=["Lesson"])
def delete_my_lesson(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    with session:
        cancel_lesson = session.get(Lesson, lesson_id)
        if not cancel_lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        if cancel_lesson.year != 2024 or cancel_lesson.season != 1:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Outdated")
        user = session.exec(select(User).where(User.username == current_user.username)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.lessons.remove(cancel_lesson)
        session.commit()
        return {"deleted": cancel_lesson}


