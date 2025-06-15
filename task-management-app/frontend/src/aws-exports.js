// このファイルは実際のデプロイ時にAmplify CLIによって自動生成されます
// 以下はサンプルの設定です

const awsmobile = {
    "aws_project_region": "us-east-1",
    "aws_cognito_identity_pool_id": "us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "aws_cognito_region": "us-east-1",
    "aws_user_pools_id": "us-east-1_xxxxxxxxx",
    "aws_user_pools_web_client_id": "xxxxxxxxxxxxxxxxxxxx",
    "oauth": {},
    "aws_cloud_logic_custom": [
        {
            "name": "TaskAPI",
            "endpoint": "https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev",
            "region": "us-east-1"
        }
    ]
};

export default awsmobile;
