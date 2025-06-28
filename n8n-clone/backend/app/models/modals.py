# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str
    name: Optional[str]
    password: str = Field(min_length=5)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    workflows: List["Workflow"] = Relationship(back_populates="user")


class Workflow(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str]
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="workflows")
    nodes: List["Node"] = Relationship(back_populates="workflow")
    connections: List["Connection"] = Relationship(back_populates="workflow")


class Node(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    workflow_id: str = Field(foreign_key="workflow.id")
    type: str
    config: dict  # JSON config
    position_x: float
    position_y: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    workflow: Optional[Workflow] = Relationship(back_populates="nodes")


class Connection(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    workflow_id: str = Field(foreign_key="workflow.id")
    from_node_id: str
    to_node_id: str

    workflow: Optional[Workflow] = Relationship(back_populates="connections")


class Execution(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    workflow_id: str = Field(foreign_key="workflow.id")
    status: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None
    logs: Optional[dict]
