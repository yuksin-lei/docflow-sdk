# Makefile for Docflow SDK
# 简化常用开发命令

.PHONY: help install install-dev test test-cov test-fast lint format type-check clean docs build publish dev hooks

# 默认目标：显示帮助信息
help:
	@echo "Docflow SDK - 开发工具"
	@echo ""
	@echo "常用命令："
	@echo "  make install      - 安装基础依赖"
	@echo "  make install-dev  - 安装开发依赖"
	@echo "  make dev          - 完整开发环境设置"
	@echo "  make test         - 运行测试"
	@echo "  make test-cov     - 运行测试并生成覆盖率报告"
	@echo "  make test-fast    - 快速测试（失败时停止）"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make type-check   - 类型检查"
	@echo "  make clean        - 清理临时文件"
	@echo "  make docs         - 生成文档"
	@echo "  make build        - 构建分发包"
	@echo "  make publish      - 发布到 PyPI"
	@echo ""

# 安装基础依赖
install:
	pip install -e .

# 安装开发依赖
install-dev:
	pip install -e ".[dev]"

# 完整开发环境设置
dev: install-dev hooks
	@echo "✓ 开发环境设置完成"

# 安装 pre-commit hooks
hooks:
	pip install pre-commit
	pre-commit install
	@echo "✓ Pre-commit hooks 已安装"

# 运行所有测试
test:
	python -m pytest

# 运行测试并生成覆盖率报告
test-cov:
	python -m pytest --cov=docflow --cov-report=html --cov-report=term-missing
	@echo "✓ 覆盖率报告已生成: htmlcov/index.html"

# 快速测试（失败时立即停止）
test-fast:
	python -m pytest -x --tb=short -v

# 运行指定的测试文件
test-file:
	@if [ -z "$(FILE)" ]; then \
		echo "用法: make test-file FILE=tests/test_client.py"; \
	else \
		python -m pytest $(FILE) -v; \
	fi

# 代码检查
lint:
	@echo "运行 Ruff 检查..."
	ruff check docflow
	@echo "运行 Black 检查..."
	black --check docflow
	@echo "✓ 代码检查完成"

# 代码格式化
format:
	@echo "运行 Black 格式化..."
	black docflow tests examples
	@echo "运行 Ruff 自动修复..."
	ruff check --fix docflow tests examples
	@echo "✓ 代码格式化完成"

# 类型检查
type-check:
	mypy docflow
	@echo "✓ 类型检查完成"

# 运行所有质量检查
check-all: lint type-check test
	@echo "✓ 所有检查通过"

# 清理临时文件
clean:
	@echo "清理临时文件..."
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	rm -rf htmlcov coverage.xml .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✓ 清理完成"

# 深度清理（包括虚拟环境）
clean-all: clean
	rm -rf .venv venv
	@echo "✓ 深度清理完成"

# 生成文档
docs:
	@if [ -d "docs" ]; then \
		cd docs && make html; \
		echo "✓ 文档已生成: docs/_build/html/index.html"; \
	else \
		echo "✗ docs 目录不存在"; \
	fi

# 构建分发包
build: clean
	pip install build
	python -m build
	@echo "✓ 构建完成: dist/"

# 发布到 PyPI（测试）
publish-test: build
	pip install twine
	twine upload --repository testpypi dist/*
	@echo "✓ 已发布到 TestPyPI"

# 发布到 PyPI（正式）
publish: build
	pip install twine
	twine upload dist/*
	@echo "✓ 已发布到 PyPI"

# 检查包
check-package: build
	pip install twine
	twine check dist/*
	@echo "✓ 包检查完成"

# 显示版本信息
version:
	@python -c "from docflow import __version__; print('Version:', __version__)"

# 显示项目统计
stats:
	@echo "项目统计信息："
	@echo "----------------"
	@echo "Python 文件数量:"
	@find docflow -name "*.py" | wc -l
	@echo "代码行数:"
	@find docflow -name "*.py" -exec wc -l {} + | tail -1
	@echo "测试文件数量:"
	@find tests -name "test_*.py" | wc -l
	@echo "示例文件数量:"
	@find examples -name "*.py" | wc -l

# 运行示例
run-example:
	@if [ -z "$(EXAMPLE)" ]; then \
		echo "用法: make run-example EXAMPLE=workspace_example"; \
		echo "可用示例:"; \
		ls examples/*.py | sed 's/examples\///g' | sed 's/.py//g'; \
	else \
		python examples/$(EXAMPLE).py; \
	fi

# Git 相关
git-status:
	@git status --short

git-commit:
	@if [ -z "$(MSG)" ]; then \
		echo "用法: make git-commit MSG='commit message'"; \
	else \
		git add -A && git commit -m "$(MSG)"; \
	fi

# 安全检查
security:
	pip install bandit safety
	bandit -r docflow
	safety check
	@echo "✓ 安全检查完成"
