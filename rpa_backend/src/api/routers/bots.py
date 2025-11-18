from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.db.models import Bot
from src.db.session import get_db

router = APIRouter(prefix="/bots", tags=["Bots"])


class BotCreate(BaseModel):
    name: str = Field(..., description="Bot name")
    workflow_id: int = Field(..., description="Associated workflow")


class BotOut(BaseModel):
    id: int
    name: str
    status: str
    workflow_id: int

    class Config:
        from_attributes = True


@router.get("/", summary="List bots", response_model=List[BotOut])
def list_bots(db: Session = Depends(get_db)) -> Any:
    return db.query(Bot).all()


@router.post("/", summary="Create bot", response_model=BotOut, status_code=status.HTTP_201_CREATED)
def create_bot(payload: BotCreate, db: Session = Depends(get_db)) -> Any:
    bot = Bot(name=payload.name, workflow_id=payload.workflow_id, status="idle")
    db.add(bot)
    db.flush()
    return bot


@router.get("/{bot_id}", summary="Get bot", response_model=BotOut)
def get_bot(bot_id: int, db: Session = Depends(get_db)) -> Any:
    bot = db.query(Bot).get(bot_id)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot not found")
    return bot
