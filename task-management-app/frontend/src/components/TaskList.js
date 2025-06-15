import React from 'react';
import { List, Card, Tag, Button, Popconfirm, Typography, Space } from 'antd';
import { EditOutlined, DeleteOutlined, CheckOutlined, ClockCircleOutlined } from '@ant-design/icons';
import moment from 'moment';

const { Title, Text } = Typography;

const getStatusTag = (status) => {
  switch (status) {
    case '未着手':
      return <Tag color="default">未着手</Tag>;
    case '進行中':
      return <Tag color="processing">進行中</Tag>;
    case '完了':
      return <Tag color="success">完了</Tag>;
    default:
      return <Tag color="default">{status}</Tag>;
  }
};

const TaskList = ({ tasks, onEdit, onDelete, loading }) => {
  return (
    <List
      grid={{ gutter: 16, xs: 1, sm: 1, md: 2, lg: 3, xl: 3, xxl: 4 }}
      dataSource={tasks}
      loading={loading}
      renderItem={(task) => (
        <List.Item>
          <Card
            title={
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Text ellipsis style={{ maxWidth: '70%' }} title={task.title}>
                  {task.title}
                </Text>
                {getStatusTag(task.status)}
              </div>
            }
            actions={[
              <Button
                type="text"
                icon={<EditOutlined />}
                onClick={() => onEdit(task)}
              >
                編集
              </Button>,
              <Popconfirm
                title="このタスクを削除しますか？"
                onConfirm={() => onDelete(task.task_id)}
                okText="はい"
                cancelText="いいえ"
              >
                <Button
                  type="text"
                  danger
                  icon={<DeleteOutlined />}
                >
                  削除
                </Button>
              </Popconfirm>,
            ]}
          >
            <div style={{ minHeight: '100px' }}>
              <Text type="secondary" ellipsis={{ rows: 3 }}>
                {task.description || '説明なし'}
              </Text>
              
              {task.due_date && (
                <div style={{ marginTop: '16px' }}>
                  <Space>
                    <ClockCircleOutlined />
                    <Text type={moment(task.due_date).isBefore(moment(), 'day') && task.status !== '完了' ? 'danger' : 'secondary'}>
                      期限: {moment(task.due_date).format('YYYY/MM/DD')}
                    </Text>
                  </Space>
                </div>
              )}
            </div>
          </Card>
        </List.Item>
      )}
      locale={{ emptyText: 'タスクがありません' }}
    />
  );
};

export default TaskList;
