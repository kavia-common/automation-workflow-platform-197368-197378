from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base


class User(Base):
    """Represents a platform user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    workflows: Mapped[list["Workflow"]] = relationship("Workflow", back_populates="owner")


class Workflow(Base):
    """Automation workflow definition and metadata."""

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    definition_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="workflows")

    bots: Mapped[list["Bot"]] = relationship("Bot", back_populates="workflow")
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="workflow")
    executions: Mapped[list["Execution"]] = relationship("Execution", back_populates="workflow")


class Bot(Base):
    """Represents an automation bot that can execute a workflow or tasks."""

    __tablename__ = "bots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="idle")

    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), nullable=False)
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="bots")


class Schedule(Base):
    """Represents a schedule for running a workflow."""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cron: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), nullable=False)
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="schedules")


class Execution(Base):
    """Represents a workflow execution instance."""

    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), nullable=False)
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="executions")

    task_runs: Mapped[list["TaskRun"]] = relationship("TaskRun", back_populates="execution")


class TaskRun(Base):
    """Represents an individual task run within an execution."""

    __tablename__ = "task_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    execution_id: Mapped[int] = mapped_column(ForeignKey("executions.id"), nullable=False)
    execution: Mapped["Execution"] = relationship("Execution", back_populates="task_runs")
