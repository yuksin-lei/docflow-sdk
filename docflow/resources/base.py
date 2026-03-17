"""
资源基类
"""
from typing import Any
from ..exceptions import ValidationError


class BaseResource:
    """资源操作基类"""

    def __init__(self, http_client: Any):
        """
        初始化资源类

        Args:
            http_client: HTTP 客户端实例
        """
        self.http_client = http_client

    def _validate_workspace_id(self, workspace_id: str) -> None:
        """
        验证工作空间 ID

        Args:
            workspace_id: 工作空间 ID

        Raises:
            ValidationError: 工作空间 ID 无效
        """
        if not workspace_id or not workspace_id.strip():
            raise ValidationError(
                "工作空间 ID 不能为空",
                i18n_key='error.workspace.id_empty'
            )

        # 验证是否可以转换为 long 型
        try:
            int(workspace_id)
        except ValueError:
            raise ValidationError(
                "工作空间 ID 格式错误，必须是数字",
                i18n_key='error.workspace.id_invalid'
            )

    def _validate_id(self, id_value: str, id_name: str) -> None:
        """
        验证 ID

        Args:
            id_value: ID 值
            id_name: ID 名称（用于错误消息）

        Raises:
            ValidationError: ID 无效
        """
        if not id_value or not id_value.strip():
            raise ValidationError(
                f"{id_name}不能为空",
                i18n_key='error.validation.empty',
                field=id_name
            )

        # 验证是否可以转换为 long 型
        try:
            int(id_value)
        except ValueError:
            raise ValidationError(
                f"{id_name}格式错误，必须是数字",
                i18n_key='error.validation.invalid_format',
                field=id_name
            )

    def _validate_page_params(self, page: int, page_size: int) -> None:
        """
        验证分页参数

        Args:
            page: 页码
            page_size: 每页数量

        Raises:
            ValidationError: 分页参数无效
        """
        if page < 1:
            raise ValidationError(
                "页码必须大于等于 1",
                i18n_key='error.workspace.page_invalid'
            )

        if page_size < 1 or page_size > 100:
            raise ValidationError(
                "每页数量必须在 1-100 之间",
                i18n_key='error.workspace.page_size_invalid'
            )
