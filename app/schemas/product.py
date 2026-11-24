from typing import Optional
from pydantic import BaseModel

# שדות בסיסיים שמשותפים ליצירה/עדכון
class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int = 0
    description: Optional[str] = None
    warehouse_id: Optional[int] = None


# סכמה המשמשת ליצירת מוצר חדש (מה שהלקוח שולח)
class ProductCreate(ProductBase):
    pass

# סכמה לעדכון מוצר (הכל אופציונלי כי אפשר לעדכן רק שדה אחד)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    warehouse_id: Optional[int] = None

# סכמה שחוזרת ללקוח (כוללת גם את ה-ID שנוצר במסד הנתונים)
class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True # מאפשר המרה אוטומטית מאובייקט SQLModel ל-Pydantic