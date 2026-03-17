"""
异常类测试
"""
import pytest
from docflow.exceptions import (
    DocflowException,
    AuthenticationError,
    ValidationError,
    ResourceNotFoundError,
    PermissionDeniedError,
    APIError,
    NetworkError
)


class TestExceptions:
    """异常类测试"""

    def test_base_exception(self):
        """测试基础异常"""
        exc = DocflowException("测试错误")
        assert str(exc) == "测试错误"
        assert isinstance(exc, Exception)

    def test_authentication_error(self):
        """测试认证错误"""
        exc = AuthenticationError()
        # i18n 翻译后的默认消息
        assert "认证失败" in str(exc)
        assert isinstance(exc, DocflowException)

    def test_validation_error(self):
        """测试参数校验错误"""
        exc = ValidationError("参数错误")
        assert str(exc) == "参数错误"
        assert isinstance(exc, DocflowException)

    def test_resource_not_found_error(self):
        """测试资源不存在错误"""
        exc = ResourceNotFoundError("资源不存在")
        assert str(exc) == "资源不存在"
        assert isinstance(exc, DocflowException)

    def test_permission_denied_error(self):
        """测试权限不足错误"""
        exc = PermissionDeniedError("权限不足")
        assert str(exc) == "权限不足"
        assert isinstance(exc, DocflowException)

    def test_api_error(self):
        """测试 API 错误"""
        exc = APIError(
            status_code=400,
            message="API 调用失败",
            code="BAD_REQUEST"
        )
        assert exc.status_code == 400
        assert exc.code == "BAD_REQUEST"
        # i18n 可能会翻译错误消息,所以只验证属性存在
        assert str(exc)  # 确保能转成字符串
        assert isinstance(exc, DocflowException)

    def test_api_error_without_optional_params(self):
        """测试 API 错误（无可选参数）"""
        exc = APIError(status_code=500, message="服务器内部错误")
        assert exc.status_code == 500
        assert exc.code is None

    def test_network_error(self):
        """测试网络错误"""
        exc = NetworkError("网络超时")
        # i18n 会翻译成"网络错误"
        assert "网络" in str(exc)
        assert isinstance(exc, DocflowException)

    def test_exception_hierarchy(self):
        """测试异常继承层次"""
        # 所有自定义异常都应该继承自 DocflowException
        exceptions = [
            AuthenticationError,
            ValidationError,
            ResourceNotFoundError,
            PermissionDeniedError,
            APIError,
            NetworkError
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, DocflowException)
            assert issubclass(exc_class, Exception)

    def test_catch_specific_exception(self):
        """测试捕获特定异常"""
        def raise_validation_error():
            raise ValidationError("参数错误")

        with pytest.raises(ValidationError) as exc_info:
            raise_validation_error()

        assert "参数错误" in str(exc_info.value)

    def test_catch_base_exception(self):
        """测试捕获基础异常"""
        def raise_api_error():
            raise APIError(status_code=500, message="API 错误")

        # 应该能用基类捕获
        with pytest.raises(DocflowException):
            raise_api_error()

    def test_exception_attributes(self):
        """测试异常属性"""
        exc = APIError(
            status_code=500,
            message="错误消息",
            code="INTERNAL_ERROR"
        )

        assert hasattr(exc, 'message')
        assert hasattr(exc, 'status_code')
        assert hasattr(exc, 'code')
        assert exc.status_code == 500
        assert exc.code == "INTERNAL_ERROR"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
