import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from backend.domain.entities.task import Task
from backend.domain.services.task_service import TaskService
from backend.domain.value_objects.task_status import TaskStatus
from backend.application.use_cases.task_use_cases import TaskUseCases
from backend.application.dtos.task_dto import TaskDTO


class TestTaskUseCases(unittest.TestCase):
    def setUp(self):
        # モックの設定
        self.mock_task_repository = Mock()
        self.task_service = TaskService(self.mock_task_repository)
        self.task_use_cases = TaskUseCases(self.task_service)
        
        # テスト用のタスク
        self.test_task = Task(
            task_id="test-task-id",
            title="テストタスク",
            description="これはテストタスクです",
            status=TaskStatus.NOT_STARTED,
            due_date=datetime(2023, 12, 31),
            user_id="test-user-id",
            created_at=datetime(2023, 1, 1),
            updated_at=datetime(2023, 1, 1)
        )
        
        # テスト用のDTO
        self.test_task_dto = TaskDTO(
            task_id="test-task-id",
            title="テストタスク",
            description="これはテストタスクです",
            status=TaskStatus.NOT_STARTED.value,
            due_date=datetime(2023, 12, 31).isoformat(),
            user_id="test-user-id",
            created_at=datetime(2023, 1, 1).isoformat(),
            updated_at=datetime(2023, 1, 1).isoformat()
        )
    
    def test_create_task(self):
        # createのモック設定
        self.mock_task_repository.save.return_value = self.test_task
        
        # テスト実行
        result = self.task_use_cases.create_task(self.test_task_dto)
        
        # 検証
        self.mock_task_repository.save.assert_called_once()
        self.assertEqual(result.task_id, self.test_task_dto.task_id)
        self.assertEqual(result.title, self.test_task_dto.title)
        self.assertEqual(result.description, self.test_task_dto.description)
        self.assertEqual(result.status, self.test_task_dto.status)
        self.assertEqual(result.due_date, self.test_task_dto.due_date)
        self.assertEqual(result.user_id, self.test_task_dto.user_id)
    
    def test_get_task(self):
        # find_by_idのモック設定
        self.mock_task_repository.find_by_id.return_value = self.test_task
        
        # テスト実行
        result = self.task_use_cases.get_task("test-task-id", "test-user-id")
        
        # 検証
        self.mock_task_repository.find_by_id.assert_called_once_with("test-task-id", "test-user-id")
        self.assertEqual(result.task_id, self.test_task_dto.task_id)
        self.assertEqual(result.title, self.test_task_dto.title)
    
    def test_get_all_tasks(self):
        # find_all_by_user_idのモック設定
        self.mock_task_repository.find_all_by_user_id.return_value = [self.test_task]
        
        # テスト実行
        result = self.task_use_cases.get_all_tasks("test-user-id")
        
        # 検証
        self.mock_task_repository.find_all_by_user_id.assert_called_once_with("test-user-id")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].task_id, self.test_task_dto.task_id)
        self.assertEqual(result[0].title, self.test_task_dto.title)
    
    def test_update_task(self):
        # find_by_idとsaveのモック設定
        self.mock_task_repository.find_by_id.return_value = self.test_task
        self.mock_task_repository.save.return_value = self.test_task
        
        # テスト実行
        result = self.task_use_cases.update_task(self.test_task_dto)
        
        # 検証
        self.mock_task_repository.save.assert_called_once()
        self.assertEqual(result.task_id, self.test_task_dto.task_id)
        self.assertEqual(result.title, self.test_task_dto.title)
    
    def test_delete_task(self):
        # find_by_idとdeleteのモック設定
        self.mock_task_repository.find_by_id.return_value = self.test_task
        self.mock_task_repository.delete.return_value = True
        
        # テスト実行
        result = self.task_use_cases.delete_task("test-task-id", "test-user-id")
        
        # 検証
        self.mock_task_repository.find_by_id.assert_called_once_with("test-task-id", "test-user-id")
        self.mock_task_repository.delete.assert_called_once_with("test-task-id", "test-user-id")
        self.assertTrue(result)
    
    def test_update_task_status(self):
        # find_by_idとsaveのモック設定
        self.mock_task_repository.find_by_id.return_value = self.test_task
        self.mock_task_repository.save.return_value = self.test_task
        
        # テスト実行
        new_status = TaskStatus.IN_PROGRESS.value
        result = self.task_use_cases.update_task_status("test-task-id", "test-user-id", new_status)
        
        # 検証
        self.mock_task_repository.find_by_id.assert_called_once_with("test-task-id", "test-user-id")
        self.mock_task_repository.save.assert_called_once()
        self.assertEqual(result.status, new_status)


if __name__ == "__main__":
    unittest.main()
