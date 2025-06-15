import { API } from 'aws-amplify';

// タスク関連のAPI呼び出し
export const TaskAPI = {
  // すべてのタスクを取得
  getAllTasks: async () => {
    try {
      return await API.get('TaskAPI', '/tasks');
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // 特定のタスクを取得
  getTask: async (taskId) => {
    try {
      return await API.get('TaskAPI', `/tasks/${taskId}`);
    } catch (error) {
      console.error(`Error fetching task ${taskId}:`, error);
      throw error;
    }
  },

  // 新しいタスクを作成
  createTask: async (taskData) => {
    try {
      return await API.post('TaskAPI', '/tasks', {
        body: taskData
      });
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  // タスクを更新
  updateTask: async (taskId, taskData) => {
    try {
      return await API.put('TaskAPI', `/tasks/${taskId}`, {
        body: taskData
      });
    } catch (error) {
      console.error(`Error updating task ${taskId}:`, error);
      throw error;
    }
  },

  // タスクを削除
  deleteTask: async (taskId) => {
    try {
      return await API.del('TaskAPI', `/tasks/${taskId}`);
    } catch (error) {
      console.error(`Error deleting task ${taskId}:`, error);
      throw error;
    }
  }
};
