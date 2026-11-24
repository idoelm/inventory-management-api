from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from app.core.config import settings

# connects_args נדרש רק עבור SQLite כדי לנהל Multi-threading
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, echo=True, connect_args=connect_args)

def init_db() -> None:
    """יוצר את הטאבלאות במסד הנתונים אם הן לא קיימות"""
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency המספק Session פעיל מול ה-DB וסוגר אותו בסיום Request"""
    with Session(engine) as session:
        yield session