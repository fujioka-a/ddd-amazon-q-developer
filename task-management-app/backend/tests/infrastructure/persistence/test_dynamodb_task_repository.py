import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from backend.domain.entities.task import Task
from backend.domain.value_objects.task_status import TaskStatus
from backend.infrastructure.persistence.dynamodb_task_repository import DynamoDBTaskRepository


class TestDynamoDBTaskRepository(unittest.TestCase):
    @patch('boto3.resource')
    def setUp(self, mock_boto3_resource):
        # DynamoDBのモック設定
        self.mock_table = MagicMock()
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = self.mock_table
        mock_boto3_resource.return_value = mock_dynamodb
        
        # リポジトリのインスタンス化
        self.repository = DynamoDBTaskRepository()
        
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
        
        # テスト用のタスク辞書
        self.test_task_dict = {
            "task_id": "test-task-id",
            "title": "テストタスク",
            "description": "これはテストタスクです",
            "status": TaskStatus.NOT_STARTED.value,
            "due_date": datetime(2023, 12, 31).isoformat(),
            "user_id": "test-user-id",
            "created_at": datetime(2023, 1, 1).isoformat(),
            "updated_at": datetime(2023, 1, 1).isoformat()
        }
    
    def test_save(self):
        # put_itemのモック設定
        self.mock_table.put_item.return_value = {}
        
        # テスト実行
        result = self.repository.save(self.test_task)
        
        # 検証
        self.mock_table.put_item.assert_called_once()
        self.assertEqual(result.task_id, self.test_task.task_id)
        self.assertEqual(result.title, self.test_task.title)
    
    def test_find_by_id(self):
        # get_itemのモック設定
        self.mock_table.get_item.return_value = {"Item": self.test_task_dict}
        
        # テスト実行
        result = self.repository.find_by_id("test-task-id", "test-user-id")
        
        # 検証
        self.mock_table.get_item.assert_called_once_with(
            Key={
                'task_id': "test-task-id",
                'user_id': "test-user-id"
            }
        )
        self.assertEqual(result.task_id, self.test_task.task_id)
        self.assertEqual(result.title, self.test_task.title)
    
    def test_find_by_id_not_found(self):
        # get_itemのモック設定（アイテムなし）
        self.mock_table.get_item.return_value = {}
        
        # テスト実行
        result = self.repository.find_by_id("test-task-id", "test-user-id")
        
        # 検証
        self.mock_table.get_item.assert_called_once()
        self.assertIsNone(result)
    
    def test_find_all_by_user_id(self):
        # queryのモック設定
        self.mock_table.query.return_value = {"Items": [self.test_task_dict]}
        
        # テスト実行
        result = self.repository.find_all_by_user_id("test-user-id")
        
        # 検証
        self.mock_table.query.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].task_id, self.test_task.task_id)
        self.assertEqual(result[0].title, self.test_task.title)
    
    def test_delete(self):
        # delete_itemのモック設定
        self.mock_table.delete_item.return_value = {"Attributes": self.test_task_dict}
        
        # テスト実行
        result = self.repository.delete("test-task-id", "test-user-id")
        
        # 検証
        self.mock_table.delete_item.assert_called_once_with(
            Key={
                'task_id': "test-task-id",
                'user_id': "test-user-id"
            },
            ReturnValues='ALL_OLD'
        )
        self.assertTrue(result)
    
    def test_delete_not_found(self):
        # delete_itemのモック設定（アイテムなし）
        self.mock_table.delete_item.return_value = {}
        
        # テスト実行
        result = self.repository.delete("test-task-id", "test-user-id")
        
        # 検証
        self.mock_table.delete_item.assert_called_once()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
