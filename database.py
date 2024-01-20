# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil


# env1 = "IN_DOCKER_CONTAINER"
env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"


db_file = 'database.sqlite'


remote_db = f"/mount/{db_file}"
local_db = db_file


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


db_connection = f'sqlite:///{local_db}'


# database settings
engine = create_engine(db_connection, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

