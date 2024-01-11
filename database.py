# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os


volume1_foler = os.path.join(os.getcwd(), "volume1")

if os.path.isdir(volume1_foler):
    db_file = 'sqlite:///volume1/database.sqlite'
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


