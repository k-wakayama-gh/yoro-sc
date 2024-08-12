# --- routers/html.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated
from datetime import datetime, timedelta

# my modules
from database import engine, get_session
from models.items import Item, ItemCreate, ItemRead, ItemUpdate, ItemDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete
from models.todos import Todo, TodoCreate, TodoRead, TodoUpdate, TodoDelete
from routers.auth import get_current_active_user
from database import make_backup_db

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# routes below 000000000000000000000000000000000000


# top page
@router.get("/", response_class=HTMLResponse, tags=["html"])
def index(request: Request):
    context = {
        "request": request,
        "title": "ホーム｜(一社)養老スポーツクラブ",
    }
    return templates.TemplateResponse("index.html", context)



# my page
@router.get("/my", response_class=HTMLResponse, tags=["html"])
def my(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("my.html", context)



# user sign up page
@router.get("/users/signup", response_class=HTMLResponse, tags=["html"])
def user_signup(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("signup.html", context)



# after sign up complete page
@router.get("/signupcomplete", response_class=HTMLResponse, tags=["html"])
def signup_complete(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("signupcomplete.html", context)



# admin top page
@router.get("/admin", response_class=HTMLResponse, tags=["html"])
def signup_complete(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("admin.html", context)




# # coffee page
# @router.get("/coffee", response_class=HTMLResponse, tags=["html"])
# def coffee(request: Request):
#     context = {
#         'request': request,
#     }
#     return templates.TemplateResponse('coffee.html', context)


# warm cold start
@router.get("/warmup")
def warmup():
    return {"warmup": "ok"}



# backup database.sqlite
@router.get("/backupdatabase")
def backup_database():
    make_backup_db()
    return {"backup database.sqlite to yoro-sc.sqlite": "ok"}



@router.get("/now", tags=["test"])
def show_current_datetime():
    current_datetime = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%dT%H-%M-%S")
    return {"now": current_datetime}

