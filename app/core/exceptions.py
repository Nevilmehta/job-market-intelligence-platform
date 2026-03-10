# This gives us project-level custom exceptions.

class AppException(Exception):
    # Base application execution
    pass

class DuplicateRawJobException(AppException):
    # Raised when a raw job with the same source and external_id already exists
    pass