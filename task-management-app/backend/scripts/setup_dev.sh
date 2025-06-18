#!/bin/bash

# 開発環境のセットアップスクリプト

# uvのインストール確認
if ! command -v uv &> /dev/null
then
    echo "uvがインストールされていません。インストールします..."
    pip install uv
fi

# 仮想環境の作成
echo "仮想環境を作成しています..."
python -m venv .venv

# 仮想環境のアクティベート
echo "仮想環境をアクティベートしています..."
source .venv/bin/activate

# 開発用依存関係のインストール
echo "開発用依存関係をインストールしています..."
uv pip install -r requirements-dev.txt

# pre-commitのインストールと設定
echo "pre-commitをインストールしています..."
pre-commit install

echo "開発環境のセットアップが完了しました！"
echo "開発を始めるには: source .venv/bin/activate"
