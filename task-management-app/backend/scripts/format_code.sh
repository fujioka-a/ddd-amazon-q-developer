#!/bin/bash

# コードフォーマットスクリプト

# 仮想環境のアクティベート（必要な場合）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ruffを使用してコードをフォーマット
echo "Ruffでコードをフォーマットしています..."
ruff format .

echo "コードのフォーマットが完了しました！"
