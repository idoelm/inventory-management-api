from fastapi import APIRouter
from app.api.v1.endpoints import products
from app.api.v1.endpoints import warehouses
from app.api.v1.endpoints import transactions

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(warehouses.router)
api_router.include_router(transactions.router)