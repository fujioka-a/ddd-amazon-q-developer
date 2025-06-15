from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.task import Task


class TaskRepository(ABC):
    """タスクリポジトリのインターフェース"""

    @abstractmethod
    def save(self, task: Task) -> Task:
        """タスクを保存する"""
        pass

    @abstractmethod
    def find_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """IDによるタスクの検索"""
        pass

    @abstractmethod
    def find_all_by_user_id(self, user_id: str) -> List[Task]:
        """ユーザーIDに基づくすべてのタスクの取得"""
        pass

    @abstractmethod
    def delete(self, task_id: str, user_id: str) -> bool:
        """タスクの削除"""
        pass
