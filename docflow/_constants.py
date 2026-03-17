"""SDK 常量定义

集中定义所有常量，便于维护和修改。
"""

# ==================== API 版本 ====================
API_VERSION = "v2"
API_PREFIX = "/app-api/sip/platform/v2"

# ==================== 默认配置 ====================
DEFAULT_BASE_URL = "https://docflow.textin.com/api"
DEFAULT_TIMEOUT = 30  # 秒
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF_FACTOR = 1.0

# ==================== HTTP 配置 ====================
# 需要重试的 HTTP 状态码
RETRY_STATUS_CODES = [423, 429, 500, 503, 504, 900]

# 允许重试的 HTTP 方法
RETRY_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]

# 连接池配置
POOL_CONNECTIONS = 10
POOL_MAXSIZE = 20

# ==================== 分页配置 ====================
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 1000

# ==================== 文件限制 ====================
MAX_FILE_SIZE_MB = 100
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# 支持的文件格式
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
SUPPORTED_DOCUMENT_FORMATS = [".pdf", ".doc", ".docx", ".xls", ".xlsx"]
SUPPORTED_FILE_FORMATS = SUPPORTED_IMAGE_FORMATS + SUPPORTED_DOCUMENT_FORMATS

# ==================== 语言配置 ====================
DEFAULT_LANGUAGE = "zh_CN"
SUPPORTED_LANGUAGES = ["zh_CN", "en_US"]

# ==================== 请求头 ====================
HEADER_APP_ID = "x-ti-app-id"
HEADER_SECRET_CODE = "x-ti-secret-code"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_USER_AGENT = "User-Agent"

# ==================== User Agent ====================
USER_AGENT_TEMPLATE = "docflow-sdk-python/{version}"

# ==================== 超时设置 ====================
CONNECT_TIMEOUT = 10  # 连接超时
READ_TIMEOUT = 30  # 读取超时

# ==================== 字段限制 ====================
MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500
MAX_WORKSPACE_ID_LENGTH = 20
MAX_CATEGORY_ID_LENGTH = 20
