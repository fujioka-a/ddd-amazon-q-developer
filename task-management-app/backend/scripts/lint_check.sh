#!/bin/bash

# リントチェックスクリプト

# 仮想環境のアクティベート（必要な場合）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ruffを使用してリントチェック
echo "Ruffでリントチェックを実行しています..."
ruff check .

# 終了コードを保存
RUFF_EXIT=$?

# MyPyを使用して型チェック
echo "MyPyで型チェックを実行しています..."
mypy .

# 終了コードを保存
MYPY_EXIT=$?

# 両方のチェックが成功した場合のみ成功とする
if [ $RUFF_EXIT -eq 0 ] && [ $MYPY_EXIT -eq 0 ]; then
    echo "リントチェックが成功しました！"
    exit 0
else
    echo "リントチェックに失敗しました。エラーを修正してください。"
    exit 1
fi
