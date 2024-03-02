# --- main.py ---

# frameworks and libraries
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# my modules
from database import engine, create_database, load_db, save_db
import route_html, route_items, route_users, route_lessons, route_auth, route_todos

# FastAPI instance
app = FastAPI(docs_url = None, redoc_url = None, openapi_url = None)

# include API router
app.include_router(route_html.router)
app.include_router(route_items.router)
app.include_router(route_users.router)
app.include_router(route_lessons.router)
app.include_router(route_auth.router)
app.include_router(route_todos.router)


# static files settings
app.mount('/static', StaticFiles(directory='static'), name='static')

# create database on startup
@app.on_event("startup")
def on_startup():
    create_database()

@app.on_event("shutdown")
def on_shutdown():
    pass

# run
if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)


# --- security for docs ---

# modules
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json")
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)


