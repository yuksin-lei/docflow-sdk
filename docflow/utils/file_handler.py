"""
文件处理工具
"""
import os
from typing import Union, BinaryIO, List, Tuple, Dict


class FileHandler:
    """文件处理工具类"""

    @staticmethod
    def prepare_file(
        file: Union[str, BinaryIO, bytes], field_name: str = "file"
    ) -> Tuple[str, Tuple[str, BinaryIO, str]]:
        """
        准备单个文件用于上传

        Args:
            file: 文件路径、文件对象或字节数据
            field_name: 表单字段名

        Returns:
            Tuple[str, Tuple[str, BinaryIO, str]]: (字段名, (文件名, 文件对象, MIME类型))

        Examples:
            >>> # 使用文件路径
            >>> FileHandler.prepare_file("/path/to/file.pdf")

            >>> # 使用文件对象
            >>> with open("/path/to/file.pdf", "rb") as f:
            ...     FileHandler.prepare_file(f)
        """
        if isinstance(file, str):
            # 文件路径
            if not os.path.exists(file):
                raise FileNotFoundError(f"文件不存在: {file}")

            filename = os.path.basename(file)
            file_obj = open(file, "rb")
            mime_type = FileHandler._guess_mime_type(filename)
            return (field_name, (filename, file_obj, mime_type))

        elif isinstance(file, bytes):
            # 字节数据
            return (field_name, ("file", file, "application/octet-stream"))

        elif hasattr(file, "read"):
            # 文件对象
            filename = getattr(file, "name", "file")
            if isinstance(filename, str):
                filename = os.path.basename(filename)
            mime_type = FileHandler._guess_mime_type(filename)
            return (field_name, (filename, file, mime_type))

        else:
            raise ValueError(f"不支持的文件类型: {type(file)}")

    @staticmethod
    def prepare_files(
        files: List[Union[str, BinaryIO, bytes]], field_name: str = "files"
    ) -> List[Tuple[str, Tuple[str, BinaryIO, str]]]:
        """
        准备多个文件用于上传

        Args:
            files: 文件列表（路径、文件对象或字节数据）
            field_name: 表单字段名

        Returns:
            List[Tuple]: 文件列表，格式为 [(字段名, (文件名, 文件对象, MIME类型)), ...]

        Examples:
            >>> files = ["/path/to/file1.pdf", "/path/to/file2.pdf"]
            >>> FileHandler.prepare_files(files, "sample_files")
        """
        prepared_files = []
        for file in files:
            prepared_files.append(FileHandler.prepare_file(file, field_name))
        return prepared_files

    @staticmethod
    def _guess_mime_type(filename: str) -> str:
        """
        根据文件名猜测 MIME 类型

        Args:
            filename: 文件名

        Returns:
            str: MIME 类型
        """
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".txt": "text/plain",
            ".json": "application/json",
            ".xml": "application/xml",
            ".zip": "application/zip",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls": "application/vnd.ms-excel",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        return mime_types.get(ext, "application/octet-stream")

    @staticmethod
    def validate_file_size(file: Union[str, BinaryIO], max_size_mb: int = 10) -> bool:
        """
        校验文件大小

        Args:
            file: 文件路径或文件对象
            max_size_mb: 最大文件大小（MB）

        Returns:
            bool: 是否通过校验

        Raises:
            ValueError: 文件超过大小限制
        """
        max_size_bytes = max_size_mb * 1024 * 1024

        if isinstance(file, str):
            size = os.path.getsize(file)
        elif hasattr(file, "seek") and hasattr(file, "tell"):
            current_pos = file.tell()
            file.seek(0, 2)  # 移动到文件末尾
            size = file.tell()
            file.seek(current_pos)  # 恢复原位置
        else:
            return True  # 无法判断大小，放行

        if size > max_size_bytes:
            raise ValueError(
                f"文件大小 {size / 1024 / 1024:.2f}MB 超过限制 {max_size_mb}MB"
            )

        return True
