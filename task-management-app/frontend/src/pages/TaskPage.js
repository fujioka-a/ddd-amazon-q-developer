import React, { useState, useEffect } from 'react';
import { Layout, Typography, Button, Modal, message, Tabs } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { API, Auth } from 'aws-amplify';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';

const { Content } = Layout;
const { Title } = Typography;
const { TabPane } = Tabs;

const TaskPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [activeTab, setActiveTab] = useState('all');

  // タスク一覧を取得
  const fetchTasks = async () => {
    setLoading(true);
    try {
      const apiName = 'TaskAPI';
      const path = '/tasks';
      const response = await API.get(apiName, path);
      setTasks(response);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      message.error('タスクの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // 初回レンダリング時にタスク一覧を取得
  useEffect(() => {
    fetchTasks();
  }, []);

  // タスク作成・更新処理
  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const apiName = 'TaskAPI';
      
      if (editingTask) {
        // 既存タスクの更新
        const path = `/tasks/${editingTask.task_id}`;
        await API.put(apiName, path, { body: values });
        message.success('タスクを更新しました');
      } else {
        // 新規タスクの作成
        const path = '/tasks';
        await API.post(apiName, path, { body: values });
        message.success('タスクを作成しました');
      }
      
      // モーダルを閉じてタスク一覧を再取得
      setModalVisible(false);
      setEditingTask(null);
      fetchTasks();
    } catch (error) {
      console.error('Error saving task:', error);
      message.error('タスクの保存に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // タスク削除処理
  const handleDelete = async (taskId) => {
    setLoading(true);
    try {
      const apiName = 'TaskAPI';
      const path = `/tasks/${taskId}`;
      await API.del(apiName, path);
      message.success('タスクを削除しました');
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
      message.error('タスクの削除に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // タスク編集モーダルを表示
  const handleEdit = (task) => {
    setEditingTask(task);
    setModalVisible(true);
  };

  // 新規タスク作成モーダルを表示
  const showCreateModal = () => {
    setEditingTask(null);
    setModalVisible(true);
  };

  // モーダルを閉じる
  const handleCancel = () => {
    setModalVisible(false);
    setEditingTask(null);
  };

  // タブに応じたタスクをフィルタリング
  const getFilteredTasks = () => {
    switch (activeTab) {
      case 'not-started':
        return tasks.filter(task => task.status === '未着手');
      case 'in-progress':
        return tasks.filter(task => task.status === '進行中');
      case 'completed':
        return tasks.filter(task => task.status === '完了');
      default:
        return tasks;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh', padding: '24px' }}>
      <Content style={{ background: '#fff', padding: '24px', borderRadius: '4px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
          <Title level={2}>タスク管理</Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={showCreateModal}
          >
            新規タスク
          </Button>
        </div>

        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="すべて" key="all" />
          <TabPane tab="未着手" key="not-started" />
          <TabPane tab="進行中" key="in-progress" />
          <TabPane tab="完了" key="completed" />
        </Tabs>

        <TaskList
          tasks={getFilteredTasks()}
          onEdit={handleEdit}
          onDelete={handleDelete}
          loading={loading}
        />

        <Modal
          title={editingTask ? 'タスクを編集' : '新規タスク作成'}
          open={modalVisible}
          onCancel={handleCancel}
          footer={null}
        >
          <TaskForm
            task={editingTask}
            onSubmit={handleSubmit}
            loading={loading}
          />
        </Modal>
      </Content>
    </Layout>
  );
};

export default TaskPage;
