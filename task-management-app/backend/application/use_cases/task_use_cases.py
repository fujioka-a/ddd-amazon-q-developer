from datetime import datetime
from typing import List, Optional

from ...domain.entities.task import Task
from ...domain.services.task_service import TaskService
from ...domain.value_objects.task_status import TaskStatus
from ..dtos.task_dto import TaskDTO


class TaskUseCases:
    """タスク関連のユースケース"""

    def __init__(self, task_service: TaskService):
        self._task_service = task_service

    def create_task(self, task_dto: TaskDTO) -> TaskDTO:
        """新しいタスクを作成する"""
        task = task_dto.to_entity()
        created_task = self._task_service.create_task(task)
        return TaskDTO.from_entity(created_task)

    def get_task(self, task_id: str, user_id: str) -> Optional[TaskDTO]:
        """特定のタスクを取得する"""
        task = self._task_service._task_repository.find_by_id(task_id, user_id)
        return TaskDTO.from_entity(task) if task else None

    def get_all_tasks(self, user_id: str) -> List[TaskDTO]:
        """ユーザーのすべてのタスクを取得する"""
        tasks = self._task_service._task_repository.find_all_by_user_id(user_id)
        return [TaskDTO.from_entity(task) for task in tasks]

    def update_task(self, task_dto: TaskDTO) -> TaskDTO:
        """タスクを更新する"""
        task = task_dto.to_entity()
        updated_task = self._task_service.update_task(task)
        return TaskDTO.from_entity(updated_task)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """タスクを削除する"""
        return self._task_service.delete_task(task_id, user_id)

    def update_task_status(self, task_id: str, user_id: str, status: str) -> TaskDTO:
        """タスクのステータスを更新する"""
        task = self._task_service._task_repository.find_by_id(task_id, user_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        task.update_status(TaskStatus(status))
        updated_task = self._task_service._task_repository.save(task)
        return TaskDTO.from_entity(updated_task)
