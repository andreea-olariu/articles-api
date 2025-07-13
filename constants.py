from enum import Enum


class ApiResponses(Enum):
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SUCCESS_MESSAGE = "Success"
    FAILED_TO_INSERT = 'Failed to insert'
