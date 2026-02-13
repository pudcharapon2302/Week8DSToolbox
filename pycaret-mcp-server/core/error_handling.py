import logging
from enum import Enum
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_FILE_PATH = "INVALID_FILE_PATH"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    INVALID_INPUT = "INVALID_INPUT"
    CODE_EXECUTION_ERROR = "CODE_EXECUTION_ERROR"
    TOOL_EXECUTION_ERROR = "TOOL_EXECUTION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

def handle_exception(e: Exception, error_type: ErrorType, message: str) -> Dict[str, Any]:
    import traceback
    logger.error(f"{message}: {str(e)}")
    return {
        "status": "ERROR",
        "error": error_type.value,
        "message": message,
        "details": str(e),
        "traceback": traceback.format_exc()
    }

def log_and_return_error(error_type: ErrorType, message: str) -> Dict[str, Any]:
    logger.error(f"{error_type.value}: {message}")
    return {"status": "ERROR", "error": error_type.value, "message": message}