from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.db.models import Execution
from src.db.session import get_db

router = APIRouter(prefix="/executions", tags=["Executions"])


class ExecutionCreate(BaseModel):
    workflow_id: int = Field(..., description="Workflow to execute")


class ExecutionOut(BaseModel):
    id: int
    workflow_id: int
    status: str

    class Config:
        from_attributes = True


@router.get("/", summary="List executions", response_model=List[ExecutionOut])
def list_executions(db: Session = Depends(get_db)) -> Any:
    return db.query(Execution).all()


@router.post("/", summary="Create execution", response_model=ExecutionOut, status_code=status.HTTP_201_CREATED)
def create_execution(payload: ExecutionCreate, db: Session = Depends(get_db)) -> Any:
    execution = Execution(workflow_id=payload.workflow_id, status="running", started_at=datetime.utcnow())
    db.add(execution)
    db.flush()
    return execution


@router.get("/{execution_id}", summary="Get execution", response_model=ExecutionOut)
def get_execution(execution_id: int, db: Session = Depends(get_db)) -> Any:
    exec_ = db.query(Execution).get(execution_id)
    if not exec_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
    return exec_
