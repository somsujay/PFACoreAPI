# app/routes/items.py
from fastapi import APIRouter, HTTPException
from app.db import crud

router = APIRouter()

@router.get("/items/")
async def read_items():
    items = await crud.fetch_items()
    return items

@router.post("/items/")
async def create_item(item: dict):
    try:
        await crud.create_item(item)
        return {"message": "Item created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
