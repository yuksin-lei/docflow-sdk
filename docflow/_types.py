"""类型别名定义

为常用类型提供语义化的别名，提升代码可读性和类型安全性。
"""
from typing import Union, Dict, Any, List, BinaryIO, TYPE_CHECKING
from os import PathLike

if TYPE_CHECKING:
    from typing import TypeAlias
else:
    try:
        from typing import TypeAlias
    except ImportError:
        # Python 3.8/3.9 兼容
        TypeAlias = type

# 文件路径类型
FilePath: TypeAlias = Union[str, PathLike]

# 文件类型（路径或文件对象）
FileInput: TypeAlias = Union[str, PathLike, BinaryIO]

# JSON 相关类型
JSONDict: TypeAlias = Dict[str, Any]
JSONValue: TypeAlias = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JSONList: TypeAlias = List[JSONValue]

# HTTP 相关类型
Headers: TypeAlias = Dict[str, str]
QueryParams: TypeAlias = Dict[str, Union[str, int, float, bool]]

# ID 类型（通常是字符串）
WorkspaceID: TypeAlias = str
CategoryID: TypeAlias = str
FileID: TypeAlias = str
TaskID: TypeAlias = str
RepoID: TypeAlias = str
GroupID: TypeAlias = str
RuleID: TypeAlias = str
