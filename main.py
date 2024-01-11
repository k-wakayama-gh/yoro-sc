# --- main.py ---

# frameworks and libraries
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# my modules
from database import engine, create_database
import route_html, route_items, route_users, route_lessons, route_auth, route_todos

# FastAPI instance
app = FastAPI()

# include API router
app.include_router(route_html.router)
app.include_router(route_items.router)
app.include_router(route_users.router)
app.include_router(route_lessons.router)
app.include_router(route_auth.router)
app.include_router(route_todos.router)


# static files settings
app.mount('/assets', StaticFiles(directory='assets'), name='static')

# create database on startup
@app.on_event("startup")
def on_startup():
    create_database()

# run
if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)


