from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.db.models import Schedule
from src.db.session import get_db

router = APIRouter(prefix="/schedules", tags=["Schedules"])


class ScheduleCreate(BaseModel):
    workflow_id: int = Field(..., description="Workflow to schedule")
    cron: str = Field(..., description="Cron expression")


class ScheduleOut(BaseModel):
    id: int
    workflow_id: int
    cron: str
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/", summary="List schedules", response_model=List[ScheduleOut])
def list_schedules(db: Session = Depends(get_db)) -> Any:
    return db.query(Schedule).all()


@router.post("/", summary="Create schedule", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db)) -> Any:
    sched = Schedule(workflow_id=payload.workflow_id, cron=payload.cron, is_active=True)
    db.add(sched)
    db.flush()
    return sched


@router.get("/{schedule_id}", summary="Get schedule", response_model=ScheduleOut)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)) -> Any:
    sched = db.query(Schedule).get(schedule_id)
    if not sched:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return sched
