from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.common.mongo import get_db


class Widget(BaseModel):
    name: str
    description: str
    quantity: int


router = APIRouter(prefix="/widgets")
logger = getLogger(__name__)


@router.post("", status_code=201)
async def create_widget(widget: Widget, db=Depends(get_db)):
    """
    Create a new widget in the database.
    """
    logger.info("Creating new widget: %s", widget.name)
    result = await db.widgets.insert_one(widget.model_dump())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create widget")
    return {"id": str(result.inserted_id), "message": "Widget created successfully"}


@router.get("", response_model=list[Widget])
async def get_widgets(db=Depends(get_db)):
    """
    Retrieve all widgets from the database.
    """
    logger.info("Retrieving all widgets")
    cursor = db.widgets.find({}, {"_id": 0})
    return await cursor.to_list(length=None)
