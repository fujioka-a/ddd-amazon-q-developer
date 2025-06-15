# タスク管理アプリケーション - インフラストラクチャ

このディレクトリには、タスク管理アプリケーションのインフラストラクチャ定義が含まれています。AWS SAM（Serverless Application Model）テンプレートを使用して、必要なAWSリソースを定義しています。

## アーキテクチャ概要

このアプリケーションは、以下のAWSサービスを使用するサーバーレスアーキテクチャで構築されています：

- **AWS Lambda**: バックエンドロジックの実行
- **Amazon API Gateway**: RESTful APIエンドポイント
- **Amazon DynamoDB**: データの永続化
- **Amazon Cognito**: ユーザー認証と認可
- **AWS Amplify**: フロントエンドのホスティングと統合

## インフラストラクチャ・アズ・コード

`template.yaml`ファイルは、AWS SAMテンプレートで、以下のリソースを定義しています：

### DynamoDB テーブル

タスクデータを保存するためのDynamoDBテーブル：

- プライマリキー: `task_id` (ハッシュキー) と `user_id` (レンジキー)
- グローバルセカンダリインデックス: `UserIdIndex` (ユーザーIDによるクエリ用)
- オンデマンドキャパシティモード

### Cognito ユーザープール

ユーザー認証のためのCognitoユーザープール：

- Eメールによる認証
- パスワードポリシー
- ユーザープールクライアント
- IDプール

### Lambda 関数

バックエンドロジックを実行するLambda関数：

- Python 3.9ランタイム
- タスク関連のAPIエンドポイントのハンドリング
- DynamoDBとCognitoへのアクセス権限

### API Gateway

RESTful APIを提供するAPI Gateway：

- CORSサポート
- Cognito認証
- タスク関連のエンドポイント

### Amplify アプリケーション

フロントエンドをホスティングするAmplifyアプリケーション：

- ビルド設定
- デプロイ設定

## デプロイ方法

### 前提条件

- AWS CLI
- AWS SAM CLI
- 適切なAWS認証情報

### デプロイ手順

1. SAMテンプレートをビルドします：

```bash
sam build
```

2. インタラクティブモードでデプロイします：

```bash
sam deploy --guided
```

3. プロンプトに従って、必要なパラメータを入力します：
   - スタック名
   - AWS リージョン
   - 環境（dev/prod）
   - 確認プロンプト

### パラメータ

テンプレートは以下のパラメータを受け付けます：

- `Environment`: 環境名（dev/prod）

### 出力

デプロイ後、以下の出力が得られます：

- `TaskApiEndpoint`: API GatewayのエンドポイントURL
- `UserPoolId`: CognitoユーザープールID
- `UserPoolClientId`: CognitoユーザープールクライアントID
- `IdentityPoolId`: CognitoアイデンティティプールID
- `TaskTableName`: DynamoDBテーブル名

## セキュリティ

このインフラストラクチャ設定には、以下のセキュリティ対策が含まれています：

- Cognitoによる認証と認可
- 最小権限の原則に基づくIAMロール
- API GatewayのCognito認証統合
- DynamoDBのユーザーごとのデータ分離

## スケーラビリティ

このアーキテクチャは、以下の理由により高いスケーラビリティを提供します：

- サーバーレスアーキテクチャ（Lambda）
- DynamoDBのオンデマンドキャパシティ
- マネージドサービスの使用

## コスト最適化

このアーキテクチャは、以下の理由によりコスト効率が高いです：

- サーバーレスアーキテクチャ（使用分のみ課金）
- DynamoDBのオンデマンドキャパシティ（トラフィックに応じた課金）
- マネージドサービスの使用（運用コストの削減）

## 運用と監視

以下のAWSサービスを使用して、アプリケーションを監視できます：

- CloudWatch Logs: Lambda関数のログ
- CloudWatch Metrics: パフォーマンスメトリクス
- X-Ray: 分散トレーシング

## カスタマイズ

テンプレートは、以下の方法でカスタマイズできます：

- 環境変数の追加
- リソース設定の変更
- スケーリングパラメータの調整
- 追加のAWSサービスの統合
