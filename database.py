# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os


azure_storage = "/azstorage1"

if os.path.isdir(azure_storage):
    db_file = f'sqlite:///{azure_storage}/database.sqlite'
else:
    db_file = 'sqlite:///database.sqlite'


# database settings
engine = create_engine(db_file, echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


