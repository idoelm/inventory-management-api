from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.db import init_db
from app.api.api import api_router
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.transaction import Transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Inventory Management API",
    docs_url="/",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} is running!"}