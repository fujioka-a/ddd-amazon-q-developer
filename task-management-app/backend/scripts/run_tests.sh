#!/bin/bash

# テスト実行スクリプト

# 仮想環境のアクティベート（必要な場合）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Pytestを使用してテストを実行
echo "テストを実行しています..."
pytest --cov=backend tests/ -v

# カバレッジレポートの生成
echo "カバレッジレポートを生成しています..."
pytest --cov=backend --cov-report=html tests/

echo "テストが完了しました！"
echo "カバレッジレポートは htmlcov/index.html で確認できます。"
