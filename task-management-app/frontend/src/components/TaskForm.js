import React, { useState, useEffect } from 'react';
import { Button, Form, Input, DatePicker, Select, message } from 'antd';
import dayjs from 'dayjs';

const { TextArea } = Input;
const { Option } = Select;

const TaskForm = ({ task, onSubmit, loading }) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (task) {
      // タスクが提供された場合、フォームにデータを設定
      form.setFieldsValue({
        title: task.title,
        description: task.description,
        status: task.status,
        due_date: task.due_date ? dayjs(task.due_date) : null,
      });
    } else {
      // 新規作成の場合はフォームをリセット
      form.resetFields();
    }
  }, [task, form]);

  const handleSubmit = (values) => {
    const formattedValues = {
      ...values,
      due_date: values.due_date ? values.due_date.format('YYYY-MM-DD') : null,
    };

    onSubmit(formattedValues);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={{
        status: '未着手',
      }}
    >
      <Form.Item
        name="title"
        label="タイトル"
        rules={[{ required: true, message: 'タイトルを入力してください' }]}
      >
        <Input placeholder="タスクのタイトル" />
      </Form.Item>

      <Form.Item
        name="description"
        label="説明"
      >
        <TextArea
          placeholder="タスクの説明（任意）"
          autoSize={{ minRows: 3, maxRows: 6 }}
        />
      </Form.Item>

      <Form.Item
        name="status"
        label="ステータス"
        rules={[{ required: true, message: 'ステータスを選択してください' }]}
      >
        <Select placeholder="ステータスを選択">
          <Option value="未着手">未着手</Option>
          <Option value="進行中">進行中</Option>
          <Option value="完了">完了</Option>
        </Select>
      </Form.Item>

      <Form.Item
        name="due_date"
        label="期限"
      >
        <DatePicker
          style={{ width: '100%' }}
          format="YYYY-MM-DD"
          placeholder="期限を選択（任意）"
        />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          {task ? 'タスクを更新' : 'タスクを作成'}
        </Button>
      </Form.Item>
    </Form>
  );
};

export default TaskForm;
