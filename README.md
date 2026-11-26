# Inventory Management API

מערכת Backend לניהול מלאי שנבנתה ב-Python עם FastAPI, SQLModel ו-Pydantic, עם מסד נתונים SQLite.

## יכולות עיקריות
* ניהול מחסנים (`Warehouses`) ומוצרים (`Products`).
* תיעוד תנועות מלאי (`IN` / `OUT`) עם עדכון אוטומטי של כמות המוצר.
* וולידציות קלט ולוגיקה עסקית (בדיקת קיום מוצר ומחסן, מניעת מלאי שלילי, כמות חיובית).
* סינון תנועות לפי `product_id`, `warehouse_id` ו-`transaction_type`.
* בדיקות אוטומטיות ב-`pytest` ו-`TestClient` עם מסד נתונים מבודד בזיכרון (`sqlite://`) כדי לא לפגוע ב-`inventory.db`.

## מבנה הפרויקט
* `app/core` – הגדרות וחיבור למסד הנתונים.
* `app/models` – מודלי SQLModel של הטבלאות.
* `app/schemas` – סכמות Pydantic לקלט ופלט.
* `app/crud` – לוגיקת הגישה לנתונים והעדכונים.
* `app/api` – ראוטרים ונקודות הקצה (Endpoints).
* `tests` – בדיקות אוטומטיות (`conftest.py`, `test_health.py`, `test_inventory.py`).

## התקנה והרצה מקומית
הפקודות תואמות ל-Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload