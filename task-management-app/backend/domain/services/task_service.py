from ..repositories.task_repository import TaskRepository
from ..entities.task import Task


class TaskService:
    """タスクに関するドメインサービス"""

    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def create_task(self, task: Task) -> Task:
        """新しいタスクを作成する"""
        return self._task_repository.save(task)

    def update_task(self, task: Task) -> Task:
        """既存のタスクを更新する"""
        existing_task = self._task_repository.find_by_id(task.task_id, task.user_id)
        if not existing_task:
            raise ValueError(f"Task with ID {task.task_id} not found")
        return self._task_repository.save(task)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """タスクを削除する"""
        existing_task = self._task_repository.find_by_id(task_id, user_id)
        if not existing_task:
            raise ValueError(f"Task with ID {task_id} not found")
        return self._task_repository.delete(task_id, user_id)
