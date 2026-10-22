from enum import Enum

class ErrorType(Enum):
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    AUTH_ERROR = "auth_error"
    BAD_REQUEST = "bad_request"
    TIMEOUT = "timeout"

class ProviderError(Exception):
    def __init__(self, error_type: ErrorType, message:str):
        super().__init__(message)
        self.error_type = error_type

def should_fallback(error_type: ErrorType) -> bool: 
    return error_type in {
        ErrorType.RATE_LIMIT,
        ErrorType.SERVER_ERROR,
        ErrorType.TIMEOUT,
    }


