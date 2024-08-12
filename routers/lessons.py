# --- routers/lessons.py ---

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
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete, UserChild
from routers.auth import get_current_active_user

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

start_time = datetime(year=2024, month=9, day=11, hour=7, minute=0, second=0, tzinfo=timezone(timedelta(hours=9)))

year = 2024
season = 2


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
        lessons = session.exec(select(Lesson).where(Lesson.year == year, Lesson.season == season)).all()
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
        lessons = session.exec(select(Lesson).where(Lesson.year == year, Lesson.season == season)).all()
        return lessons




# get: read a lesson
@router.get("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def read_lesson(session: Annotated[Session, Depends(get_session)], lesson_id: int):
    lesson = session.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Not found")
    return lesson



# patch: update lesson information
@router.patch("/lessons/{lesson_id}", response_model=LessonRead, tags=["Lesson"])
def update_lesson(lesson_id: int, lesson_update: LessonUpdate, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        db_lesson = session.get(Lesson, lesson_id)
        if not db_lesson:
            raise HTTPException(status_code=404, detail="Not found")
        
        lesson_update_dict = lesson_update.model_dump(exclude_unset=True)
        
        for key, value in lesson_update_dict.items():
            setattr(db_lesson, key, value)
            
        session.add(db_lesson)
        session.commit()
        session.refresh(db_lesson)
        return db_lesson



# delete: cancel a lesson
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




# get: read my lessons
@router.get("/json/my/lessons", response_model=list[LessonRead], tags=["Lesson"])
def read_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        my_lessons = user.lessons
        return my_lessons



# post: sign up to a lessons
@router.post("/lessons/{id}", response_model=list[LessonRead], tags=["Lesson"])
def create_my_lessons(current_user: Annotated[UserRead, Depends(get_current_active_user)], id: int):
    current_time = (datetime.utcnow() + timedelta(hours=9)).replace(tzinfo=timezone(timedelta(hours=9)))
    if current_time < start_time and current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="lesson signup is not allowed yet")
    with Session(engine) as session:
        new_lesson = session.exec(select(Lesson).where(Lesson.id == id)).one()
        if new_lesson.year != year or new_lesson.season != season:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        if not new_lesson in user.lessons:
            user.lessons.append(new_lesson)
            session.add(user)
            session.commit()
            session.refresh(user)
        if new_lesson.number == 1: # subject to change: lessons for children
            user_children = session.exec(select(UserChild).where(UserChild.user_id == user.id)).all()
            for child in user_children:
                if not new_lesson in child.lessons:
                    child.lessons.append(new_lesson)
            new_lesson.capacity_left = new_lesson.capacity - len(new_lesson.user_children)
            session.add(new_lesson)
            session.commit()
            session.refresh(new_lesson)
        else:
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



# admin: display admin lessons async for management
@router.get("/admin/lessons", response_class=HTMLResponse, tags=["Lesson"], response_model=list[LessonRead])
def display_superuser_lessons(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("admin/lessons.html", context)



# delete: cancel a lesson
@router.delete("/my/lessons/{lesson_id}", tags=["Lesson"])
def delete_my_lesson(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        cancel_lesson = session.get(Lesson, lesson_id)
        if not cancel_lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        if cancel_lesson.year != year or cancel_lesson.season != season:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Outdated")
        user = session.exec(select(User).where(User.username == current_user.username)).one()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user in cancel_lesson.users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not signed up")
        if cancel_lesson in user.lessons:
            user.lessons.remove(cancel_lesson)
            session.add(user)
            session.commit()
            session.refresh(user)
        if cancel_lesson.number == 1: # subject to change: lessons for children
            user_children = session.exec(select(UserChild).where(UserChild.user_id == user.id)).all()
            for child in user_children:
                child.lessons.remove(cancel_lesson)
            cancel_lesson.capacity_left = cancel_lesson.capacity - len(cancel_lesson.user_children)
            session.add(cancel_lesson)
            session.commit()
            session.refresh(cancel_lesson)
            return {"removed": cancel_lesson}
        else:
            cancel_lesson.capacity_left = cancel_lesson.capacity - len(cancel_lesson.users)
            session.add(cancel_lesson)
            session.commit()
            session.refresh(cancel_lesson)
            return {"removed": cancel_lesson}




# admin: read user list of a lesson
@router.get("/json/admin/lessons/{lesson_id}/users", response_model=list[UserRead], tags={"Lesson"})
def admin_json_read_users_of_a_lesson(lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
        lesson_member = lesson.users
        return lesson_member




# admin: json: read lesson member list
@router.get("/json/admin/lessons/users", tags={"Lesson"})
def admin_json_read_users_of_every_lessons(current_user: Annotated[User, Depends(get_current_active_user)], year: int = None, season: int = None):
    # if current_user.username != "user":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        accessing_user = session.exec(select(User).where(User.username == current_user.username)).one()
        if accessing_user.is_admin != True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        
        if year and season:
            lessons = session.exec(select(Lesson).where(Lesson.year == year and Lesson.season == season)).all()
        elif year and not season:
            lessons = session.exec(select(Lesson).where(Lesson.year == year)).all()
        else:
            lessons = session.exec(select(Lesson)).all()
        lessons_users_list = []
        for lesson in lessons:
            users = []
            if lesson.id == 1:
                for child in lesson.user_children:
                    parent = session.exec(select(User).where(User.id == child.user_id)).one()
                    child_dict = child.model_dump()
                    parent_name = parent.user_details.last_name + "　" + parent.user_details.first_name
                    parent_tel = parent.user_details.tel
                    parent_postal_code = parent.user_details.postal_code
                    parent_address = parent.user_details.address
                    child_dict["parent_name"] = parent_name
                    child_dict["parent_tel"] = parent_tel
                    child_dict["parent_postal_code"] = parent_postal_code
                    child_dict["parent_address"] = parent_address
                    users.append(child_dict)
            else:
                for user in lesson.users:
                    user_details = user.user_details
                    users.append(user_details)
            lessons_users_dict = {"lesson_id": lesson.id, "lesson_title": lesson.title, "users": users}
            lessons_users_list.append(lessons_users_dict)
        return lessons_users_list




# admin: display lesson member list
@router.get("/admin/lessons/users", tags={"Lesson"})
def admin_display_users_of_every_lessons(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("admin/lessonmember.html", context)




# admin: delete: remove a user from a lesson
@router.delete("/admin/users/{username}/remove/{lesson_id}", tags=["Lesson"])
def admin_remove_lesson_member(username: str, lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
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
        message = f"{username}：{user_fullname}を「{lesson_title}」から削除しました。"
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
            elif lesson.number != 1:
                user_position = lesson_member.index(user) + 1
            elif lesson.number == 1:
                user_children = session.exec(select(UserChild).where(UserChild.user_id == user.id)).all()
                user_position = 0
                for child in user_children:
                    if child in lesson.user_children:
                        user_position = lesson.user_children.index(child) + 1
            positioon_dict = {"lesson_id": lesson.id, "user_position": user_position}
            position_list.append(positioon_dict)
        return position_list




# admin: read: lesson list of a user signed up
@router.get("/json/admin/user/{user_id}/lessons", tags=["Lesson"])
def admin_json_read_user_lesson_list(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    with Session(engine) as session:
        user = session.get(User, user_id)
        user_lessons = user.lessons
        return user_lessons



# admin: post: sign up to a lessons
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




# admin: temorary function
@router.get("/admin/user/{user_id}/lesson/{lesson_id}/enter-children", tags=["Lesson"])
def admin_add_children_into_lesson(user_id: int, lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if lesson_id != 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="lesson_id must be 1")
    with Session(engine) as session:
        user = session.get(User, user_id)
        user_children = user.user_children
        lesson = session.get(Lesson, lesson_id)
        if user in lesson.users:
            for child in user_children:
                if not child in lesson.user_children:
                    child.lessons.append(lesson)
            lesson.capacity_left = lesson.capacity - len(lesson.user_children)
            session.add(lesson)
            session.commit()
            session.refresh(lesson)
            return {"children signed up to the lesson": "done"}
        else:
            return {"parent user has not signed up to the lesson": "ignored"}



# admin: temorary function username ver
@router.get("/admin/user/{username}/lesson/{lesson_id}/enter-children-username-ver", tags=["Lesson"])
def admin_add_children_into_lesson_username_ver(username: str, lesson_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    if current_user.username != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    if lesson_id != 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="lesson_id must be 1")
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).one()
        user_children = user.user_children
        lesson = session.get(Lesson, lesson_id)
        if user in lesson.users:
            for child in user_children:
                if not child in lesson.user_children:
                    child.lessons.append(lesson)
            lesson.capacity_left = lesson.capacity - len(lesson.user_children)
            session.add(lesson)
            session.commit()
            session.refresh(lesson)
            return {"children signed up to the lesson": "done"}
        else:
            return {"parent user has not signed up to the lesson": "ignored"}




# get: refresh lesson capacity
@router.get("/lessons/refresh/capacity", tags=["Lesson"])
def refresh_lesson_capacity_left(session: Annotated[Session, Depends(get_session)]):
    lessons = session.exec(select(Lesson).where(Lesson.year == 2024)).all()
    for lesson in lessons:
        lesson.capacity_left = lesson.capacity - len(lesson.users)
        session.add(lesson)
    session.commit()
    for lesson in lessons:
        session.refresh(lesson)
    return lessons



# get: json list of lesson applicants
@router.get("/json/lessons/{lesson_id}/applicants", tags=["Lesson"])
def json_read_lesson_applicants(lesson_id: int, session: Annotated[Session, Depends(get_session)]):
    lesson = session.exec(select(Lesson).where(Lesson.id == lesson_id)).one()
    result = []
    if lesson.id == 1:
        user_children = lesson.user_children
        counter = 1
        for child in user_children:
            user_details = child.user.user_details
            child_details_out = {"No.": counter, "name": child.child_last_name + "　" + child.child_first_name, "parent": user_details.last_name + "　" + user_details.first_name, "tel": user_details.tel}
            counter = counter + 1
            result.append(child_details_out)
    else:
        users = lesson.users
        counter = 1
        for user in users:
            user_details = user.user_details
            user_details_out = {"No.": counter, "name": (user_details.last_name + "　" + user_details.first_name), "tel": user_details.tel}
            counter = counter + 1
            result.append(user_details_out)
    return result


