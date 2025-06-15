import unittest
from datetime import datetime
from uuid import uuid4

from backend.domain.entities.task import Task
from backend.domain.value_objects.task_status import TaskStatus


class TestTask(unittest.TestCase):
    def test_create_task(self):
        # タスク作成のテスト
        task_id = str(uuid4())
        title = "テストタスク"
        description = "これはテストタスクです"
        status = TaskStatus.NOT_STARTED
        due_date = datetime(2023, 12, 31)
        user_id = "test-user-id"
        
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            user_id=user_id
        )
        
        self.assertEqual(task.task_id, task_id)
        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.status, status)
        self.assertEqual(task.due_date, due_date)
        self.assertEqual(task.user_id, user_id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
    
    def test_update_task(self):
        # タスク更新のテスト
        task = Task(
            title="元のタイトル",
            description="元の説明",
            status=TaskStatus.NOT_STARTED,
            user_id="test-user-id"
        )
        
        # 更新前の状態を保存
        original_updated_at = task.updated_at
        
        # 少し待ってから更新
        import time
        time.sleep(0.001)
        
        # タスクを更新
        new_title = "新しいタイトル"
        new_description = "新しい説明"
        new_status = TaskStatus.IN_PROGRESS
        new_due_date = datetime(2023, 12, 31)
        
        task.update_title(new_title)
        task.update_description(new_description)
        task.update_status(new_status)
        task.update_due_date(new_due_date)
        
        # 更新後の検証
        self.assertEqual(task.title, new_title)
        self.assertEqual(task.description, new_description)
        self.assertEqual(task.status, new_status)
        self.assertEqual(task.due_date, new_due_date)
        self.assertNotEqual(task.updated_at, original_updated_at)
    
    def test_to_dict(self):
        # to_dictメソッドのテスト
        task_id = str(uuid4())
        title = "テストタスク"
        description = "これはテストタスクです"
        status = TaskStatus.NOT_STARTED
        due_date = datetime(2023, 12, 31)
        user_id = "test-user-id"
        created_at = datetime(2023, 1, 1)
        updated_at = datetime(2023, 1, 2)
        
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            user_id=user_id,
            created_at=created_at,
            updated_at=updated_at
        )
        
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["task_id"], task_id)
        self.assertEqual(task_dict["title"], title)
        self.assertEqual(task_dict["description"], description)
        self.assertEqual(task_dict["status"], status.value)
        self.assertEqual(task_dict["due_date"], due_date.isoformat())
        self.assertEqual(task_dict["user_id"], user_id)
        self.assertEqual(task_dict["created_at"], created_at.isoformat())
        self.assertEqual(task_dict["updated_at"], updated_at.isoformat())
    
    def test_from_dict(self):
        # from_dictメソッドのテスト
        task_id = str(uuid4())
        title = "テストタスク"
        description = "これはテストタスクです"
        status = TaskStatus.NOT_STARTED.value
        due_date = datetime(2023, 12, 31).isoformat()
        user_id = "test-user-id"
        created_at = datetime(2023, 1, 1).isoformat()
        updated_at = datetime(2023, 1, 2).isoformat()
        
        task_dict = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "status": status,
            "due_date": due_date,
            "user_id": user_id,
            "created_at": created_at,
            "updated_at": updated_at
        }
        
        task = Task.from_dict(task_dict)
        
        self.assertEqual(task.task_id, task_id)
        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.status, TaskStatus.NOT_STARTED)
        self.assertEqual(task.due_date.isoformat(), due_date)
        self.assertEqual(task.user_id, user_id)
        self.assertEqual(task.created_at.isoformat(), created_at)
        self.assertEqual(task.updated_at.isoformat(), updated_at)


if __name__ == "__main__":
    unittest.main()
