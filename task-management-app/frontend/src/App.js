import React from 'react';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { ConfigProvider } from 'antd';
import jaJP from 'antd/lib/locale/ja_JP';
import 'antd/dist/reset.css'; // antd v5以降はreset.cssを使用
import './App.css';
import TaskPage from './pages/TaskPage';
import awsconfig from './aws-exports';

// Amplify設定
Amplify.configure(awsconfig);

function App({ signOut, user }) {
  return (
    <ConfigProvider locale={jaJP}>
      <div className="App">
        <header className="App-header">
          <div className="user-info">
            <span className="user-name">
              {user?.username || 'ゲスト'} としてログイン中
            </span>
            <button onClick={signOut} className="sign-out-button">
              サインアウト
            </button>
          </div>
        </header>
        <TaskPage />
      </div>
    </ConfigProvider>
  );
}

export default withAuthenticator(App);
