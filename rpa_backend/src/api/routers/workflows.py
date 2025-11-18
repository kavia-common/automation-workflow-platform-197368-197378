from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.db.models import Workflow
from src.db.session import get_db

router = APIRouter(prefix="/workflows", tags=["Workflows"])


class WorkflowCreate(BaseModel):
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = Field(None, description="Optional description")


class WorkflowOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", summary="List workflows", response_model=List[WorkflowOut])
def list_workflows(db: Session = Depends(get_db)) -> Any:
    return db.query(Workflow).all()


@router.post("/", summary="Create workflow", response_model=WorkflowOut, status_code=status.HTTP_201_CREATED)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db)) -> Any:
    wf = Workflow(name=payload.name, description=payload.description, owner_id=1)  # Placeholder owner_id
    db.add(wf)
    db.flush()
    return wf


@router.get("/{workflow_id}", summary="Get workflow", response_model=WorkflowOut)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)) -> Any:
    wf = db.query(Workflow).get(workflow_id)
    if not wf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return wf
