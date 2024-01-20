# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil

db_file = 'database.sqlite'

# env1 = "IN_DOCKER_CONTAINER"
env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"

if env in os.environ:
    db_dir = "/home/db_dir"
    db_path = f"{db_dir}/{db_file}"
else:
    db_dir = ""
    db_path = f"{db_file}"


remote_db = f"{db_dir}/{db_file}"
local_db = f"/{db_file}"


def load_db():
    if env in os.environ:
        shutil.copy(remote_db, local_db)
    else:
        pass

def save_db():
    if env in os.environ:
        shutil.copy(local_db, remote_db)
    else:
        pass


sqlite_connection = f'sqlite:///{db_path}'

# database settings
engine = create_engine(sqlite_connection, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

