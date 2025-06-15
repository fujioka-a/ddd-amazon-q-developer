import unittest
import json
from unittest.mock import Mock, patch
from datetime import datetime

from backend.interfaces.api.task_api import TaskAPI
from backend.application.dtos.task_dto import TaskDTO


class TestTaskAPI(unittest.TestCase):
    def setUp(self):
        # モックの設定
        self.mock_task_use_cases = Mock()
        self.mock_auth_service = Mock()
        self.task_api = TaskAPI(self.mock_task_use_cases, self.mock_auth_service)
        
        # テスト用のDTO
        self.test_task_dto = TaskDTO(
            task_id="test-task-id",
            title="テストタスク",
            description="これはテストタスクです",
            status="未着手",
            due_date=datetime(2023, 12, 31).isoformat(),
            user_id="test-user-id",
            created_at=datetime(2023, 1, 1).isoformat(),
            updated_at=datetime(2023, 1, 1).isoformat()
        )
        
        # テスト用のイベント
        self.test_event = {
            "headers": {
                "Authorization": "Bearer test-token"
            },
            "pathParameters": {
                "taskId": "test-task-id"
            },
            "body": json.dumps({
                "title": "テストタスク",
                "description": "これはテストタスクです",
                "status": "未着手",
                "due_date": "2023-12-31"
            })
        }
        
        # 認証サービスのモック設定
        self.mock_auth_service.get_user_id_from_token.return_value = "test-user-id"
    
    def test_handle_get_all_tasks(self):
        # get_all_tasksのモック設定
        self.mock_task_use_cases.get_all_tasks.return_value = [self.test_task_dto]
        
        # テスト実行
        result = self.task_api.handle_get_all_tasks(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.get_all_tasks.assert_called_once_with("test-user-id")
        self.assertEqual(result["statusCode"], 200)
        
        # レスポンスボディの検証
        body = json.loads(result["body"])
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["task_id"], "test-task-id")
        self.assertEqual(body[0]["title"], "テストタスク")
    
    def test_handle_get_task(self):
        # get_taskのモック設定
        self.mock_task_use_cases.get_task.return_value = self.test_task_dto
        
        # テスト実行
        result = self.task_api.handle_get_task(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.get_task.assert_called_once_with("test-task-id", "test-user-id")
        self.assertEqual(result["statusCode"], 200)
        
        # レスポンスボディの検証
        body = json.loads(result["body"])
        self.assertEqual(body["task_id"], "test-task-id")
        self.assertEqual(body["title"], "テストタスク")
    
    def test_handle_create_task(self):
        # create_taskのモック設定
        self.mock_task_use_cases.create_task.return_value = self.test_task_dto
        
        # テスト実行
        result = self.task_api.handle_create_task(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.create_task.assert_called_once()
        self.assertEqual(result["statusCode"], 201)
        
        # レスポンスボディの検証
        body = json.loads(result["body"])
        self.assertEqual(body["task_id"], "test-task-id")
        self.assertEqual(body["title"], "テストタスク")
    
    def test_handle_update_task(self):
        # get_taskとupdate_taskのモック設定
        self.mock_task_use_cases.get_task.return_value = self.test_task_dto
        self.mock_task_use_cases.update_task.return_value = self.test_task_dto
        
        # テスト実行
        result = self.task_api.handle_update_task(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.get_task.assert_called_once_with("test-task-id", "test-user-id")
        self.mock_task_use_cases.update_task.assert_called_once()
        self.assertEqual(result["statusCode"], 200)
        
        # レスポンスボディの検証
        body = json.loads(result["body"])
        self.assertEqual(body["task_id"], "test-task-id")
        self.assertEqual(body["title"], "テストタスク")
    
    def test_handle_delete_task(self):
        # delete_taskのモック設定
        self.mock_task_use_cases.delete_task.return_value = True
        
        # テスト実行
        result = self.task_api.handle_delete_task(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.delete_task.assert_called_once_with("test-task-id", "test-user-id")
        self.assertEqual(result["statusCode"], 204)
    
    def test_unauthorized_request(self):
        # 認証失敗のモック設定
        self.mock_auth_service.get_user_id_from_token.return_value = None
        
        # テスト実行
        result = self.task_api.handle_get_all_tasks(self.test_event)
        
        # 検証
        self.mock_auth_service.get_user_id_from_token.assert_called_once_with("test-token")
        self.mock_task_use_cases.get_all_tasks.assert_not_called()
        self.assertEqual(result["statusCode"], 401)
        
        # レスポンスボディの検証
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "Unauthorized")


if __name__ == "__main__":
    unittest.main()
