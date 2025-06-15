from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain.entities.task import Task
from ...domain.value_objects.task_status import TaskStatus


@dataclass
class TaskDTO:
    """タスクのデータ転送オブジェクト"""
    task_id: Optional[str]
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[str]
    user_id: str
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_entity(cls, task: Task) -> "TaskDTO":
        """エンティティからDTOへの変換"""
        return cls(
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            status=task.status.value,
            due_date=task.due_date.isoformat() if task.due_date else None,
            user_id=task.user_id,
            created_at=task.created_at.isoformat() if task.created_at else None,
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
        )

    def to_entity(self) -> Task:
        """DTOからエンティティへの変換"""
        return Task(
            task_id=self.task_id,
            title=self.title,
            description=self.description,
            status=TaskStatus(self.status) if self.status else TaskStatus.NOT_STARTED,
            due_date=datetime.fromisoformat(self.due_date) if self.due_date else None,
            user_id=self.user_id,
            created_at=datetime.fromisoformat(self.created_at) if self.created_at else None,
            updated_at=datetime.fromisoformat(self.updated_at) if self.updated_at else None,
        )
