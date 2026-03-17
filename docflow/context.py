"""
上下文类，提供链式调用功能
"""
from typing import TYPE_CHECKING, Union, BinaryIO, List, Optional, Dict, Any
from .enums import AuthScope, EnabledFlag, EnabledStatus, ExtractModel
from ._constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE

if TYPE_CHECKING:
    from .utils.http_client import HTTPClient
    from .resources.workspace import WorkspaceResource
    from .resources.category import (
        CategoryResource,
        CategoryFieldResource,
        CategoryTableResource,
        CategorySampleResource,
    )
    from .resources.review import ReviewResource
    from .models.review import (
        ReviewRepoCreateResponse,
        ReviewRepoListResponse,
        ReviewRepoInfo,
        ReviewGroupCreateResponse,
        ReviewRuleCreateResponse,
    )


class CategoryContext:
    """
    类别上下文，绑定 workspace_id 和 category_id，简化 API 调用

    Examples:
        >>> # 绑定上下文后，无需重复传递 workspace_id 和 category_id
        >>> cat = client.workspace("123").category("456")
        >>>
        >>> # 字段操作
        >>> cat.fields.add(name="税率")
        >>> cat.fields.update(field_id="789", name="税率(%)")
        >>> cat.fields.list()
        >>>
        >>> # 表格操作
        >>> cat.tables.add(name="明细表")
        >>> cat.tables.list()
        >>>
        >>> # 样本操作
        >>> cat.samples.upload(file="sample.pdf")
        >>> cat.samples.list()
    """

    def __init__(
        self,
        http_client: "HTTPClient",
        category_resource: "CategoryResource",
        workspace_id: str,
        category_id: str,
    ):
        """
        初始化类别上下文

        Args:
            http_client: HTTP 客户端
            category_resource: 类别资源对象
            workspace_id: 工作空间 ID
            category_id: 类别 ID
        """
        self._http_client = http_client
        self._category_resource = category_resource
        self.workspace_id = workspace_id
        self.category_id = category_id

        # 初始化子资源上下文
        self.fields = CategoryFieldContext(
            self._category_resource.fields, workspace_id, category_id
        )
        self.tables = CategoryTableContext(
            self._category_resource.tables, workspace_id, category_id
        )
        self.samples = CategorySampleContext(
            self._category_resource.samples, workspace_id, category_id
        )

    def update(
        self,
        name: Optional[str] = None,
        category_prompt: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[Union[EnabledFlag, int]] = None,
        **kwargs,
    ) -> None:
        """
        更新类别

        Args:
            name: 新的类别名称（可选）
            category_prompt: 新的类别提示（可选）
            description: 新的描述（可选）
            enabled: 启用状态（EnabledFlag.DISABLED=0 或 EnabledFlag.ENABLED=1，可选）
            **kwargs: 其他要更新的字段
        """
        return self._category_resource.update(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            name=name,
            category_prompt=category_prompt,
            description=description,
            enabled=enabled,
            **kwargs,
        )

    def delete(self) -> None:
        """删除当前类别"""
        return self._category_resource.delete(
            workspace_id=self.workspace_id, category_ids=[self.category_id]
        )


class CategoryFieldContext:
    """类别字段上下文"""

    def __init__(
        self,
        field_resource: "CategoryFieldResource",
        workspace_id: str,
        category_id: str,
    ):
        self._field_resource = field_resource
        self.workspace_id = workspace_id
        self.category_id = category_id

    def list(self):
        """获取字段列表"""
        return self._field_resource.list(
            workspace_id=self.workspace_id, category_id=self.category_id
        )

    def add(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs,
    ):
        """新增字段"""
        return self._field_resource.add(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            name=name,
            description=description,
            **kwargs,
        )

    def get_config(self, field_id: str):
        """获取字段配置"""
        return self._field_resource.get_config(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            field_id=field_id,
        )

    def update(
        self,
        field_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs,
    ) -> None:
        """更新字段"""
        return self._field_resource.update(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            field_id=field_id,
            name=name,
            description=description,
            **kwargs,
        )

    def delete(self, field_ids: List[str]) -> None:
        """批量删除字段"""
        return self._field_resource.delete(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            field_ids=field_ids,
        )


class CategoryTableContext:
    """类别表格上下文"""

    def __init__(
        self,
        table_resource: "CategoryTableResource",
        workspace_id: str,
        category_id: str,
    ):
        self._table_resource = table_resource
        self.workspace_id = workspace_id
        self.category_id = category_id

    def list(self):
        """获取表格列表"""
        return self._table_resource.list(
            workspace_id=self.workspace_id, category_id=self.category_id
        )

    def add(
        self, name: str, description: Optional[str] = None, **kwargs
    ):
        """新增表格"""
        return self._table_resource.add(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            name=name,
            description=description,
            **kwargs,
        )

    def update(
        self,
        table_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs,
    ) -> None:
        """更新表格"""
        return self._table_resource.update(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            table_id=table_id,
            name=name,
            description=description,
            **kwargs,
        )

    def delete(self, table_ids: List[str]) -> None:
        """批量删除表格"""
        return self._table_resource.delete(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            table_ids=table_ids,
        )


class CategorySampleContext:
    """类别样本上下文"""

    def __init__(
        self,
        sample_resource: "CategorySampleResource",
        workspace_id: str,
        category_id: str,
    ):
        self._sample_resource = sample_resource
        self.workspace_id = workspace_id
        self.category_id = category_id

    def upload(self, file: Union[str, BinaryIO]):
        """上传样本文件"""
        return self._sample_resource.upload(
            workspace_id=self.workspace_id, category_id=self.category_id, file=file
        )

    def list(self, page: int = DEFAULT_PAGE, page_size: int = DEFAULT_PAGE_SIZE):
        """获取样本列表"""
        return self._sample_resource.list(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            page=page,
            page_size=page_size,
        )

    def download(self, sample_id: str, save_path: Optional[str] = None) -> bytes:
        """下载样本文件"""
        return self._sample_resource.download(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            sample_id=sample_id,
            save_path=save_path,
        )

    def delete(self, sample_ids: List[str]) -> None:
        """批量删除样本"""
        return self._sample_resource.delete(
            workspace_id=self.workspace_id,
            category_id=self.category_id,
            sample_ids=sample_ids,
        )


class ReviewContext:
    """
    审核规则上下文，绑定 workspace_id，简化审核规则 API 调用

    Examples:
        >>> # 绑定工作空间上下文
        >>> ws = client.workspace("123")
        >>>
        >>> # 创建审核规则库
        >>> repo = ws.review.create_repo(name="发票审核规则库")
        >>>
        >>> # 获取规则库列表
        >>> repos = ws.review.list_repos(page=1, page_size=10)
        >>>
        >>> # 创建规则组
        >>> group = ws.review.create_group(repo_id=repo.repo_id, name="金额验证")
        >>>
        >>> # 创建规则
        >>> rule = ws.review.create_rule(
        ...     group_id=group.group_id,
        ...     name="金额范围检查",
        ...     rule_type="range",
        ...     config={"field": "金额", "min": 0, "max": 100000}
        ... )
    """

    def __init__(
        self,
        review_resource: "ReviewResource",
        workspace_id: str,
    ):
        """
        初始化审核规则上下文

        Args:
            review_resource: 审核规则资源对象
            workspace_id: 工作空间 ID
        """
        self._review_resource = review_resource
        self.workspace_id = workspace_id

    def create_repo(self, name: str) -> "ReviewRepoCreateResponse":
        """
        创建审核规则库

        Args:
            name: 规则库名称

        Returns:
            ReviewRepoCreateResponse: 包含新创建的规则库信息
        """
        return self._review_resource.create_repo(
            workspace_id=self.workspace_id,
            name=name
        )

    def list_repos(self, page: int = DEFAULT_PAGE, page_size: int = 10) -> "ReviewRepoListResponse":
        """
        获取审核规则库列表

        Args:
            page: 页码，从 1 开始，默认 1
            page_size: 每页数量，默认 10

        Returns:
            ReviewRepoListResponse: 规则库列表响应
        """
        return self._review_resource.list_repos(
            workspace_id=self.workspace_id,
            page=page,
            page_size=page_size
        )

    def get_repo(self, repo_id: str) -> "ReviewRepoInfo":
        """
        获取单个规则库详情

        Args:
            repo_id: 规则库 ID

        Returns:
            ReviewRepoInfo: 规则库详细信息
        """
        return self._review_resource.get_repo(
            workspace_id=self.workspace_id,
            repo_id=repo_id
        )

    def update_repo(self, repo_id: str, name: str) -> None:
        """
        更新规则库

        Args:
            repo_id: 规则库 ID
            name: 新的规则库名称
        """
        return self._review_resource.update_repo(
            workspace_id=self.workspace_id,
            repo_id=repo_id,
            name=name
        )

    def delete_repo(self, repo_ids: List[str]) -> None:
        """
        批量删除规则库

        Args:
            repo_ids: 规则库 ID 列表
        """
        return self._review_resource.delete_repo(
            workspace_id=self.workspace_id,
            repo_ids=repo_ids
        )

    def create_group(self, repo_id: str, name: str) -> "ReviewGroupCreateResponse":
        """
        创建审核规则组

        Args:
            repo_id: 规则库 ID
            name: 规则组名称

        Returns:
            ReviewGroupCreateResponse: 包含新创建的规则组信息
        """
        return self._review_resource.create_group(
            workspace_id=self.workspace_id,
            repo_id=repo_id,
            name=name
        )

    def update_group(self, group_id: str, name: str) -> None:
        """
        更新规则组

        Args:
            group_id: 规则组 ID
            name: 新的规则组名称
        """
        return self._review_resource.update_group(
            workspace_id=self.workspace_id,
            group_id=group_id,
            name=name
        )

    def delete_group(self, group_id: str) -> None:
        """
        删除规则组

        Args:
            group_id: 规则组 ID
        """
        return self._review_resource.delete_group(
            workspace_id=self.workspace_id,
            group_id=group_id
        )

    def create_rule(
        self,
        group_id: str,
        name: str,
        rule_type: str,
        config: Dict[str, Any],
        **kwargs
    ) -> "ReviewRuleCreateResponse":
        """
        创建审核规则

        Args:
            group_id: 规则组 ID
            name: 规则名称
            rule_type: 规则类型
            config: 规则配置
            **kwargs: 其他参数

        Returns:
            ReviewRuleCreateResponse: 包含新创建的规则信息
        """
        return self._review_resource.create_rule(
            workspace_id=self.workspace_id,
            group_id=group_id,
            name=name,
            rule_type=rule_type,
            config=config,
            **kwargs
        )

    def update_rule(
        self,
        rule_id: str,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        """
        更新审核规则

        Args:
            rule_id: 规则 ID
            name: 新的规则名称（可选）
            config: 新的规则配置（可选）
            **kwargs: 其他要更新的字段
        """
        return self._review_resource.update_rule(
            workspace_id=self.workspace_id,
            rule_id=rule_id,
            name=name,
            config=config,
            **kwargs
        )

    def delete_rule(self, rule_id: str) -> None:
        """
        删除审核规则

        Args:
            rule_id: 规则 ID
        """
        return self._review_resource.delete_rule(
            workspace_id=self.workspace_id,
            rule_id=rule_id
        )


class WorkspaceContext:
    """
    工作空间上下文，绑定 workspace_id，简化 API 调用

    Examples:
        >>> # 绑定工作空间上下文
        >>> ws = client.workspace("123")
        >>>
        >>> # 获取工作空间详情
        >>> detail = ws.get()
        >>>
        >>> # 更新工作空间
        >>> ws.update(name="新名称")
        >>>
        >>> # 类别操作（链式调用）
        >>> cat = ws.category("456")
        >>> cat.fields.add(name="金额")
        >>>
        >>> # 列出类别
        >>> categories = ws.list_categories(page=1, page_size=20)
        >>>
        >>> # 审核规则操作（链式调用）
        >>> repo = ws.review.create_repo(name="发票审核规则库")
        >>> group = ws.review.create_group(repo_id=repo.repo_id, name="金额验证")
        >>> rule = ws.review.create_rule(group_id=group.group_id, name="金额范围", rule_type="range", config={})
    """

    def __init__(
        self,
        http_client: "HTTPClient",
        workspace_resource: "WorkspaceResource",
        category_resource: "CategoryResource",
        review_resource: "ReviewResource",
        workspace_id: str,
    ):
        """
        初始化工作空间上下文

        Args:
            http_client: HTTP 客户端
            workspace_resource: 工作空间资源对象
            category_resource: 类别资源对象
            review_resource: 审核规则资源对象
            workspace_id: 工作空间 ID
        """
        self._http_client = http_client
        self._workspace_resource = workspace_resource
        self._category_resource = category_resource
        self._review_resource = review_resource
        self.workspace_id = workspace_id

        # 初始化审核规则上下文
        self.review = ReviewContext(
            review_resource=self._review_resource,
            workspace_id=self.workspace_id
        )

    def get(self):
        """获取工作空间详情"""
        return self._workspace_resource.get(workspace_id=self.workspace_id)

    def update(
        self,
        name: Optional[str] = None,
        auth_scope: Optional[Union[AuthScope, int]] = None,
        **kwargs,
    ) -> None:
        """
        更新工作空间

        Args:
            name: 新的工作空间名称（可选）
            auth_scope: 新的权限范围（AuthScope.PRIVATE=0 或 AuthScope.PUBLIC=1，可选）
            **kwargs: 其他要更新的字段
        """
        return self._workspace_resource.update(
            workspace_id=self.workspace_id, name=name, auth_scope=auth_scope, **kwargs
        )

    def delete(self) -> None:
        """删除当前工作空间"""
        return self._workspace_resource.delete(workspace_ids=[self.workspace_id])

    def category(self, category_id: str) -> CategoryContext:
        """
        绑定类别上下文，实现链式调用

        Args:
            category_id: 类别 ID

        Returns:
            CategoryContext: 类别上下文对象

        Examples:
            >>> ws = client.workspace("123")
            >>> cat = ws.category("456")
            >>> cat.fields.add(name="税率")
        """
        return CategoryContext(
            http_client=self._http_client,
            category_resource=self._category_resource,
            workspace_id=self.workspace_id,
            category_id=category_id,
        )

    def list_categories(
        self, page: int = DEFAULT_PAGE, page_size: int = DEFAULT_PAGE_SIZE, enabled: Union[EnabledStatus, str] = EnabledStatus.ENABLED
    ):
        """
        获取当前工作空间的类别列表

        Args:
            page: 页码，从 1 开始，默认 1
            page_size: 每页数量，默认 20，最大 100
            enabled: 启用状态（EnabledStatus 枚举或字符串），默认 EnabledStatus.ENABLED

        Returns:
            CategoryListResponse: 类别列表响应
        """
        return self._category_resource.list(
            workspace_id=self.workspace_id, page=page, page_size=page_size, enabled=enabled
        )

    def create_category(
        self,
        name: str,
        extract_model: Union[ExtractModel, str],
        sample_files: List[Union[str, BinaryIO]],
        fields: List[Dict[str, Any]],
        tables: Optional[List[Dict[str, Any]]] = None,
        category_prompt: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        在当前工作空间创建类别

        Args:
            name: 类别名称
            extract_model: 提取模型（ExtractModel.LLM 或 ExtractModel.VLM）
            sample_files: 样本文件列表
            fields: 字段配置列表
            tables: 表格配置列表（可选）
            category_prompt: 类别提示（可选）
            description: 类别描述（可选）

        Returns:
            CategoryCreateResponse: 包含新创建的类别 ID
        """
        return self._category_resource.create(
            workspace_id=self.workspace_id,
            name=name,
            extract_model=extract_model,
            sample_files=sample_files,
            fields=fields,
            tables=tables,
            category_prompt=category_prompt,
            description=description,
        )
