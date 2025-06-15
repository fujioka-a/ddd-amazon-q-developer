import json
from datetime import datetime
from typing import Dict, Any, Optional

from ...application.dtos.task_dto import TaskDTO
from ...application.use_cases.task_use_cases import TaskUseCases
from ...infrastructure.auth.cognito_auth_service import CognitoAuthService


class TaskAPI:
    """タスクAPIのハンドラー"""

    def __init__(self, task_use_cases: TaskUseCases, auth_service: CognitoAuthService):
        self._task_use_cases = task_use_cases
        self._auth_service = auth_service

    def _get_user_id_from_event(self, event: Dict[str, Any]) -> Optional[str]:
        """イベントからユーザーIDを取得する"""
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header[7:]  # 'Bearer 'の後の部分を取得
        return self._auth_service.get_user_id_from_token(token)

    def _create_response(self, status_code: int, body: Any) -> Dict[str, Any]:
        """APIレスポンスを作成する"""
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps(body, default=str)
        }

    def handle_get_all_tasks(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """すべてのタスクを取得するハンドラー"""
        user_id = self._get_user_id_from_event(event)
        if not user_id:
            return self._create_response(401, {'message': 'Unauthorized'})
            
        tasks = self._task_use_cases.get_all_tasks(user_id)
        return self._create_response(200, [task.__dict__ for task in tasks])

    def handle_get_task(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """特定のタスクを取得するハンドラー"""
        user_id = self._get_user_id_from_event(event)
        if not user_id:
            return self._create_response(401, {'message': 'Unauthorized'})
            
        path_parameters = event.get('pathParameters', {})
        task_id = path_parameters.get('taskId')
        
        if not task_id:
            return self._create_response(400, {'message': 'Task ID is required'})
            
        task = self._task_use_cases.get_task(task_id, user_id)
        
        if not task:
            return self._create_response(404, {'message': 'Task not found'})
            
        return self._create_response(200, task.__dict__)

    def handle_create_task(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """タスクを作成するハンドラー"""
        user_id = self._get_user_id_from_event(event)
        if not user_id:
            return self._create_response(401, {'message': 'Unauthorized'})
            
        try:
            body = json.loads(event.get('body', '{}'))
            
            # 必須フィールドの検証
            if 'title' not in body:
                return self._create_response(400, {'message': 'Title is required'})
                
            task_dto = TaskDTO(
                task_id=None,
                title=body.get('title'),
                description=body.get('description'),
                status=body.get('status', 'NOT_STARTED'),
                due_date=body.get('due_date'),
                user_id=user_id,
                created_at=None,
                updated_at=None
            )
            
            created_task = self._task_use_cases.create_task(task_dto)
            return self._create_response(201, created_task.__dict__)
        except Exception as e:
            return self._create_response(500, {'message': str(e)})

    def handle_update_task(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """タスクを更新するハンドラー"""
        user_id = self._get_user_id_from_event(event)
        if not user_id:
            return self._create_response(401, {'message': 'Unauthorized'})
            
        try:
            path_parameters = event.get('pathParameters', {})
            task_id = path_parameters.get('taskId')
            
            if not task_id:
                return self._create_response(400, {'message': 'Task ID is required'})
                
            body = json.loads(event.get('body', '{}'))
            
            # 既存のタスクを取得
            existing_task = self._task_use_cases.get_task(task_id, user_id)
            if not existing_task:
                return self._create_response(404, {'message': 'Task not found'})
                
            # 更新するフィールドを設定
            task_dto = TaskDTO(
                task_id=task_id,
                title=body.get('title', existing_task.title),
                description=body.get('description', existing_task.description),
                status=body.get('status', existing_task.status),
                due_date=body.get('due_date', existing_task.due_date),
                user_id=user_id,
                created_at=existing_task.created_at,
                updated_at=None  # 更新時に自動設定される
            )
            
            updated_task = self._task_use_cases.update_task(task_dto)
            return self._create_response(200, updated_task.__dict__)
        except Exception as e:
            return self._create_response(500, {'message': str(e)})

    def handle_delete_task(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """タスクを削除するハンドラー"""
        user_id = self._get_user_id_from_event(event)
        if not user_id:
            return self._create_response(401, {'message': 'Unauthorized'})
            
        path_parameters = event.get('pathParameters', {})
        task_id = path_parameters.get('taskId')
        
        if not task_id:
            return self._create_response(400, {'message': 'Task ID is required'})
            
        try:
            result = self._task_use_cases.delete_task(task_id, user_id)
            if result:
                return self._create_response(204, {})
            else:
                return self._create_response(404, {'message': 'Task not found'})
        except Exception as e:
            return self._create_response(500, {'message': str(e)})
