# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil

env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"
# env = "IN_DOCKER_CONTAINER"
mount = "/mount"

# if env in os.environ:
#     db_file = f'sqlite:///{mount}/database.sqlite'
# else:
#     db_file = 'sqlite:///database.sqlite'

remote_db = "/mount/database.sqlite"
local_db = "/database.sqlite"

def load_db():
    shutil.copy(remote_db, local_db)

def save_db():
    shutil.copy(local_db, remote_db)


db_file = 'sqlite:///database.sqlite'

# database settings
engine = create_engine(db_file, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

