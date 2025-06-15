from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from ..value_objects.task_status import TaskStatus


class Task:
    """タスクエンティティ"""

    def __init__(
        self,
        title: str,
        user_id: str,
        task_id: Optional[str] = None,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.NOT_STARTED,
        due_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._task_id = task_id if task_id else str(uuid4())
        self._title = title
        self._description = description
        self._status = status
        self._due_date = due_date
        self._user_id = user_id
        self._created_at = created_at if created_at else datetime.now()
        self._updated_at = updated_at if updated_at else datetime.now()

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def status(self) -> TaskStatus:
        return self._status

    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_title(self, title: str) -> None:
        self._title = title
        self._updated_at = datetime.now()

    def update_description(self, description: Optional[str]) -> None:
        self._description = description
        self._updated_at = datetime.now()

    def update_status(self, status: TaskStatus) -> None:
        self._status = status
        self._updated_at = datetime.now()

    def update_due_date(self, due_date: Optional[datetime]) -> None:
        self._due_date = due_date
        self._updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "task_id": self._task_id,
            "title": self._title,
            "description": self._description,
            "status": self._status.value,
            "due_date": self._due_date.isoformat() if self._due_date else None,
            "user_id": self._user_id,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id=data.get("task_id"),
            title=data.get("title"),
            description=data.get("description"),
            status=TaskStatus(data.get("status")),
            due_date=datetime.fromisoformat(data.get("due_date")) if data.get("due_date") else None,
            user_id=data.get("user_id"),
            created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data.get("updated_at")) if data.get("updated_at") else None,
        )
