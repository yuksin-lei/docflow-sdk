"""
认证处理模块
"""
from typing import Dict
from ._constants import HEADER_APP_ID, HEADER_SECRET_CODE


class AuthHandler:
    """认证处理器，使用 x-ti-app-id 和 x-ti-secret-code 进行认证"""

    def __init__(self, app_id: str, secret_code: str):
        """
        初始化认证处理器

        Args:
            app_id: 应用ID
            secret_code: 密钥
        """
        self.app_id = app_id
        self.secret_code = secret_code

    def get_auth_headers(self) -> Dict[str, str]:
        """
        获取认证请求头

        Returns:
            Dict[str, str]: 认证请求头
        """
        headers = {}
        if self.app_id and self.secret_code:
            headers[HEADER_APP_ID] = self.app_id
            headers[HEADER_SECRET_CODE] = self.secret_code
        return headers

    def set_credentials(self, app_id: str, secret_code: str) -> None:
        """
        更新认证凭证

        Args:
            app_id: 新的应用ID
            secret_code: 新的密钥
        """
        self.app_id = app_id
        self.secret_code = secret_code
