import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.db import get_db
from app.main import app

# ודא שכל המודלים נטענים לפני create_all
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.transaction import Transaction


@pytest.fixture(name="client")
def client_fixture():
    # מסד נתונים זמני בזיכרון בלבד - לא נוגע ב-inventory.db האמיתי
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)

    def get_test_db():
        with Session(test_engine) as session:
            yield session

    # מחליפים זמנית את get_db של האפליקציה בגרסת הבדיקות
    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    # מנקים את ה-override בסיום הבדיקה
    app.dependency_overrides.clear()