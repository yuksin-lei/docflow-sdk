"""Pytest 配置和 fixtures

提供测试所需的常用 fixtures，避免重复代码。
"""
import pytest
from typing import Dict, Any
from docflow import DocflowClient


@pytest.fixture
def test_app_id() -> str:
    """测试用的 App ID"""
    return "test_app_id_123456"


@pytest.fixture
def test_secret_code() -> str:
    """测试用的 Secret Code"""
    return "test_secret_code_abcdef"


@pytest.fixture
def client(test_app_id: str, test_secret_code: str) -> DocflowClient:
    """创建测试客户端 fixture

    Returns:
        DocflowClient: 已初始化的测试客户端
    """
    return DocflowClient(
        app_id=test_app_id,
        secret_code=test_secret_code,
        base_url="https://test.api.example.com",
        max_retries=0,  # 测试时不重试
        timeout=5,
    )


@pytest.fixture
def mock_workspace_id() -> str:
    """模拟工作空间 ID"""
    return "123456789"


@pytest.fixture
def mock_category_id() -> str:
    """模拟类别 ID"""
    return "456789"


@pytest.fixture
def mock_file_id() -> str:
    """模拟文件 ID"""
    return "789012"


@pytest.fixture
def mock_repo_id() -> str:
    """模拟规则库 ID"""
    return "100001"


@pytest.fixture
def mock_group_id() -> str:
    """模拟规则组 ID"""
    return "200002"


@pytest.fixture
def mock_rule_id() -> str:
    """模拟规则 ID"""
    return "300003"


@pytest.fixture
def mock_success_response() -> Dict[str, Any]:
    """模拟成功的 API 响应"""
    return {
        "code": 200,
        "msg": "success",
        "result": {}
    }


@pytest.fixture
def mock_error_response() -> Dict[str, Any]:
    """模拟失败的 API 响应"""
    return {
        "code": 400,
        "message": "Bad Request",
        "result": None
    }


@pytest.fixture
def mock_workspace_data() -> Dict[str, Any]:
    """模拟工作空间数据"""
    return {
        "workspace_id": "123456789",
        "name": "测试工作空间",
        "enterprise_id": 12345,
        "auth_scope": 1,
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_category_data() -> Dict[str, Any]:
    """模拟类别数据"""
    return {
        "id": "456789",
        "name": "测试类别",
        "extract_model": "llm",
        "enabled": 1
    }


@pytest.fixture
def mock_file_data() -> Dict[str, Any]:
    """模拟文件数据"""
    return {
        "id": "file_123",
        "name": "test_invoice.pdf",
        "format": "pdf",
        "task_id": "task_456",
        "category": "增值税发票",
        "recognition_status": "success"
    }


@pytest.fixture
def mock_review_repo_data() -> Dict[str, Any]:
    """模拟审核规则库数据"""
    return {
        "repo_id": "repo_001",
        "name": "测试规则库",
        "groups": []
    }


# 标记定义
def pytest_configure(config):
    """配置 pytest markers"""
    config.addinivalue_line(
        "markers", "unit: 单元测试"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试（需要真实 API）"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试"
    )
