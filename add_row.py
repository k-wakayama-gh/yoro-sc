# --- add_row.py ---

# modules
from sqlmodel import SQLModel, Session, select

from database import engine
from models import items, users, lessons, todos

def add_rows():
    session = Session(engine)
    
    
    sample_item = items.Item(item_name="アイテム名", price=100, description="これはサンプルアイテムです！")
    sample_user_1 = users.User(username="johndoe", email="johndoe@example.com", full_name="John Doe", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", is_active=True)
    sample_user_2 = users.User(username="alice", email="alice@example.com", full_name="Alice Wonderson", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", is_active=False)
    sample_lesson = lessons.Lesson(number=1, title="体操", teacher="講師", day="水", time="10:00〜12:00", price=5000, description="コメント！")
    sample_todo = todos.Todo(title="サンプルタスク", content="内容がないよう")
    
    
    session.add(sample_item)
    session.add(sample_user_1)
    session.add(sample_user_2)
    session.add(sample_lesson)
    session.add(sample_todo)
    
    
    session.commit()
    
    session.close()

add_rows()


