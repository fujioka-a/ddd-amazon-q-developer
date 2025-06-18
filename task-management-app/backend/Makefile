.PHONY: install install-dev format lint test clean

# デフォルトターゲット
all: install-dev format lint test

# 依存関係のインストール
install:
	uv pip install -r requirements.txt

# 開発用依存関係のインストール
install-dev:
	uv pip install -r requirements-dev.txt

# コードフォーマット
format:
	ruff format .

# リントチェック
lint:
	ruff check .
	mypy .

# テスト実行
test:
	pytest --cov=backend tests/

# キャッシュファイルなどの削除
clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# SAMビルド
sam-build:
	cd .. && sam build -t infrastructure/template.yaml

# SAMローカル実行
sam-local:
	cd .. && sam local start-api -t infrastructure/template.yaml

# SAMデプロイ
sam-deploy:
	cd .. && sam deploy --guided -t infrastructure/template.yaml
