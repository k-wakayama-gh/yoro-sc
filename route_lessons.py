# --- route_lessons.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated

# my modules
from database import engine, get_session
from models.lessons import Lesson, LessonCreate, LessonRead, LessonUpdate, LessonDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# routes below 000000000000000000000000000000000000


# create
@router.post("/lessons", response_model=LessonRead, tags=["Lesson"])
def create_lesson(*, session: Session = Depends(get_session), lesson: LessonCreate):
    db_lesson = Lesson.from_orm(lesson)
    session.add(db_lesson)
    session.commit()
    session.refresh(db_lesson)
    return db_lesson



# read list
@router.get("/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_lessons_list(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    lessons = session.exec(select(Lesson).offset(offset).limit(limit)).all()
    if not lessons:
        raise HTTPException(status_code=404, detail="Not found")
    return lessons




# read one
@router.get("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def read_lesson(*, session: Session = Depends(get_session), lesson_id: int):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Not found")
    return lesson



# update
@router.patch("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def update_lesson(*, session: Session = Depends(get_session), lesson_id: int, lesson: LessonUpdate):
    db_lesson = session.get(Lesson, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Not found")
    lesson_data = lesson.model_dump(exclude_unset=True)
    for key, value in lesson_data.lessons():
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
    return {"ok": True}


