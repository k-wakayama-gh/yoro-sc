# --- route_html.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, Annotated

# my modules
from database import engine, get_session
from models.items import Item, ItemCreate, ItemRead, ItemUpdate, ItemDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete
from models.todos import Todo, TodoCreate, TodoRead, TodoUpdate, TodoDelete
from route_auth import get_current_active_user
from database import save_db

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
        "title": "タイトル",
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



# sign up after complete page
@router.get("/signupcomplete", response_class=HTMLResponse, tags=["html"])
def signup_complete(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("signupcomplete.html", context)



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



# # backup database.sqlite
# @router.get("/backupdatabase")
# def backup_database():
#     save_db()
#     return {"backup database.sqlite": "ok"}

