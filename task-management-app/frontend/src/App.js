import React from 'react';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { ConfigProvider } from 'antd';
import jaJP from 'antd/lib/locale/ja_JP';
import 'antd/dist/antd.css';
import TaskPage from './pages/TaskPage';
import awsconfig from './aws-exports';

// Amplify設定
Amplify.configure(awsconfig);

function App({ signOut, user }) {
  return (
    <ConfigProvider locale={jaJP}>
      <div className="App">
        <header className="App-header" style={{ background: '#f0f2f5', padding: '16px', display: 'flex', justifyContent: 'flex-end' }}>
          <div>
            <span style={{ marginRight: '16px' }}>
              {user.username} としてログイン中
            </span>
            <button onClick={signOut} style={{ cursor: 'pointer' }}>
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
