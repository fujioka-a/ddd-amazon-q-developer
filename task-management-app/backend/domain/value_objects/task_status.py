from enum import Enum


class TaskStatus(Enum):
    """タスクのステータスを表す値オブジェクト"""
    NOT_STARTED = "未着手"
    IN_PROGRESS = "進行中"
    COMPLETED = "完了"
