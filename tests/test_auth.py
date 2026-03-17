"""
认证模块测试
"""
import pytest
from docflow.auth import AuthHandler
from docflow.exceptions import AuthenticationError


class TestAuthHandler:
    """认证处理器测试"""

    def test_auth_init(self):
        """测试认证初始化"""
        auth = AuthHandler(app_id="test_id", secret_code="test_secret")
        assert auth.app_id == "test_id"
        assert auth.secret_code == "test_secret"

    def test_get_headers(self):
        """测试获取认证头"""
        auth = AuthHandler(app_id="test_id", secret_code="test_secret")
        headers = auth.get_auth_headers()

        assert "x-ti-app-id" in headers
        assert "x-ti-secret-code" in headers
        assert headers["x-ti-app-id"] == "test_id"
        assert headers["x-ti-secret-code"] == "test_secret"

    def test_set_credentials(self):
        """测试更新凭证"""
        auth = AuthHandler(app_id="old_id", secret_code="old_secret")
        auth.set_credentials("new_id", "new_secret")

        assert auth.app_id == "new_id"
        assert auth.secret_code == "new_secret"

        headers = auth.get_auth_headers()
        assert headers["x-ti-app-id"] == "new_id"
        assert headers["x-ti-secret-code"] == "new_secret"

    def test_auth_with_empty_credentials(self):
        """测试空凭证"""
        auth = AuthHandler(app_id="", secret_code="")
        headers = auth.get_auth_headers()

        # 空凭证应该返回空字典
        assert headers == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
