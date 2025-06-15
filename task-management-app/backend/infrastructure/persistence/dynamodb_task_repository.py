import os
from datetime import datetime
from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from ...domain.entities.task import Task
from ...domain.repositories.task_repository import TaskRepository
from ...domain.value_objects.task_status import TaskStatus


class DynamoDBTaskRepository(TaskRepository):
    """DynamoDBを使用したタスクリポジトリの実装"""

    def __init__(self):
        self._dynamodb = boto3.resource('dynamodb')
        self._table_name = os.environ.get('TASK_TABLE_NAME', 'Tasks')
        self._table = self._dynamodb.Table(self._table_name)

    def save(self, task: Task) -> Task:
        """タスクを保存する"""
        task_dict = task.to_dict()
        self._table.put_item(Item=task_dict)
        return task

    def find_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """IDによるタスクの検索"""
        response = self._table.get_item(
            Key={
                'task_id': task_id,
                'user_id': user_id
            }
        )
        
        item = response.get('Item')
        if not item:
            return None
            
        return Task.from_dict(item)

    def find_all_by_user_id(self, user_id: str) -> List[Task]:
        """ユーザーIDに基づくすべてのタスクの取得"""
        response = self._table.query(
            IndexName='UserIdIndex',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        
        items = response.get('Items', [])
        return [Task.from_dict(item) for item in items]

    def delete(self, task_id: str, user_id: str) -> bool:
        """タスクの削除"""
        response = self._table.delete_item(
            Key={
                'task_id': task_id,
                'user_id': user_id
            },
            ReturnValues='ALL_OLD'
        )
        
        return 'Attributes' in response
