# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os
import shutil


# env1 = "IN_DOCKER_CONTAINER"
env = "WEBSITES_ENABLE_APP_SERVICE_STORAGE"


remote_db = "/home/mount/database.sqlite"
local_db = "database.sqlite"


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



sql_connection = f'sqlite:///{local_db}'

if env in os.environ:
    sql_connection = 'Server=tcp:m9-m9-m9.database.windows.net,1433;Initial Catalog=m9-m9-m9;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;Authentication="Active Directory Default";'


# database settings
engine = create_engine(sql_connection, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

