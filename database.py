# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os


azstorage1_foler = os.path.join(os.getcwd(), "azstorage1")

if os.path.isdir(azstorage1_foler):
    db_file = 'sqlite:///azstorage1/database.sqlite'
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


