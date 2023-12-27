from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class BaseTodo(SQLModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=200)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Study FastAPI',
                'description': 'Study FastAPI tutorials with official documents.',
                'priority': 1,
                'complete': False
            }
        }
    }


class Todo(BaseTodo, table=True):
    __tablename__ = 'todos'

    id: Optional[int] = Field(primary_key=True, default=None)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    completed_at: datetime = Field(nullable=True)

    def update(self, body):
        for key, value in body.model_dump(exclude_none=True).items():
            setattr(self, key, value)
            if key == 'complete' and value == True:
                self.completed_at = datetime.utcnow()


class TodoReqeust(BaseTodo):
    pass
