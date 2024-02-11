# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil


# env1 = "IN_DOCKER_CONTAINER"
env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"

db_file = 'database.sqlite'

remote_db_dir = "/mount/db_dir/"

if env in os.environ:
    if not os.path.exists(remote_db_dir):
        os.makedirs(remote_db_dir)
        print(f"Directory {remote_db_dir} has been created.")
    else:
        print(f"Directory {remote_db_dir} already exists.")


remote_db = f"{remote_db_dir}{db_file}"


# if env in os.environ:
#     local_db = f"/home/site/wwwroot/db_dir/{db_file}"
# else:
#     local_db = db_file

local_db = db_file


# copy data
def load_db():
    if env in os.environ:
        try:
            shutil.copy(remote_db, local_db)
            print(f"Copyed {remote_db} to {local_db}")
        except:
            print("Source file not found")

def save_db():
    if env in os.environ:
        try:
            shutil.copy(local_db, remote_db)
            print(f"Copyed {local_db} to {remote_db}")
        except:
            print("Source file not found")


db_connection = f'sqlite:///{local_db}'


# database settings
engine = create_engine(db_connection, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


