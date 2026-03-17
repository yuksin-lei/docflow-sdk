"""
国际化（i18n）支持模块
"""
import os
from typing import Dict, Optional
from .._constants import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class I18nManager:
    """国际化管理器"""

    # 单例模式
    _instance: Optional['I18nManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._current_language = DEFAULT_LANGUAGE
            self._translations: Dict[str, Dict[str, str]] = {}
            self._load_translations()
            self._initialized = True

    def _load_translations(self):
        """加载所有语言翻译"""
        from .locales import zh_CN, en_US

        self._translations['zh_CN'] = zh_CN.TRANSLATIONS
        self._translations['en_US'] = en_US.TRANSLATIONS

    def set_language(self, language: str):
        """
        设置当前语言

        Args:
            language: 语言代码，如 'zh_CN', 'en_US'

        Raises:
            ValueError: 当语言不支持时
        """
        if language not in self._translations:
            raise ValueError(
                f"不支持的语言: {language}. "
                f"支持的语言: {list(self._translations.keys())}"
            )
        self._current_language = language

    def get_language(self) -> str:
        """获取当前语言"""
        return self._current_language

    def get_available_languages(self) -> list:
        """获取所有可用语言"""
        return list(self._translations.keys())

    def translate(self, key: str, **kwargs) -> str:
        """
        翻译指定的消息键

        Args:
            key: 消息键
            **kwargs: 用于格式化的参数

        Returns:
            str: 翻译后的消息
        """
        # 获取当前语言的翻译
        translations = self._translations.get(self._current_language, {})

        # 获取消息模板
        message = translations.get(key, key)

        # 格式化消息
        try:
            return message.format(**kwargs)
        except KeyError:
            # 如果格式化失败，返回原始消息
            return message

    def t(self, key: str, **kwargs) -> str:
        """translate 的简写形式"""
        return self.translate(key, **kwargs)


# 创建全局实例
i18n = I18nManager()


def set_language(language: str):
    """设置全局语言"""
    i18n.set_language(language)


def get_language() -> str:
    """获取当前语言"""
    return i18n.get_language()


def translate(key: str, **kwargs) -> str:
    """翻译消息"""
    return i18n.translate(key, **kwargs)


def t(key: str, **kwargs) -> str:
    """translate 的简写"""
    return i18n.t(key, **kwargs)


__all__ = [
    'I18nManager',
    'i18n',
    'set_language',
    'get_language',
    'translate',
    't'
]
