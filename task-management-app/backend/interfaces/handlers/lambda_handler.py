import json
import os
from typing import Dict, Any

from ...application.use_cases.task_use_cases import TaskUseCases
from ...domain.services.task_service import TaskService
from ...infrastructure.auth.cognito_auth_service import CognitoAuthService
from ...infrastructure.persistence.dynamodb_task_repository import DynamoDBTaskRepository
from ..api.task_api import TaskAPI


# 依存関係の初期化
task_repository = DynamoDBTaskRepository()
task_service = TaskService(task_repository)
task_use_cases = TaskUseCases(task_service)
auth_service = CognitoAuthService()
task_api = TaskAPI(task_use_cases, auth_service)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda関数のメインハンドラー"""
    print(f"Received event: {json.dumps(event)}")
    
    # API Gateway経由のイベントを処理
    http_method = event.get('httpMethod')
    resource = event.get('resource')
    
    # CORSプリフライトリクエストの処理
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Access-Control-Allow-Credentials': True,
            },
            'body': ''
        }
    
    # タスク関連のエンドポイントをルーティング
    if resource == '/tasks' and http_method == 'GET':
        return task_api.handle_get_all_tasks(event)
    elif resource == '/tasks' and http_method == 'POST':
        return task_api.handle_create_task(event)
    elif resource == '/tasks/{taskId}' and http_method == 'GET':
        return task_api.handle_get_task(event)
    elif resource == '/tasks/{taskId}' and http_method == 'PUT':
        return task_api.handle_update_task(event)
    elif resource == '/tasks/{taskId}' and http_method == 'DELETE':
        return task_api.handle_delete_task(event)
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'message': 'Not Found'})
        }
