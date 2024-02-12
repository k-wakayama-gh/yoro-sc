# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil


# env1 = "IN_DOCKER_CONTAINER"
env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"


if env in os.environ:
    db_file = "/home/site/wwwroot/db_dir/database.sqlite"
else:
    db_file = "database.sqlite"


db_connection = f"sqlite:///{db_file}"


# database settings
engine = create_engine(db_connection, echo=False, connect_args={'check_same_thread': False})


# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session




remote_db_dir = "/home/site/wwwroot/db_dir/"
remote_db = f"{remote_db_dir}{db_file}"
local_db = db_file


# load and save db in persist directory
def make_remote_db_dir():
    if env in os.environ:
        if not os.path.exists(remote_db_dir):
            os.makedirs(remote_db_dir)
            print(f"Directory {remote_db_dir} has been created.")
        else:
            print(f"Directory {remote_db_dir} already exists.")


def load_db():
    make_remote_db_dir()
    if os.path.exists(remote_db_dir):
        shutil.copy(remote_db, local_db)
        print(f"Copyed {remote_db} to {local_db}")
    else:
        print("Remote directory not found")


def save_db():
    make_remote_db_dir()
    if os.path.exists(remote_db_dir):
        shutil.copy(local_db, remote_db)
        print(f"Copyed {local_db} to {remote_db}")
    else:
        print("Remote directory not found")

