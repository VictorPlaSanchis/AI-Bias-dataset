from enum import Enum

class ColumnType(Enum):
    BOOLEAN = "boolean"
    CURRENCY = "currency"
    PERCENTAGE = "percentage"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    TIMESTAMP = "timestamp"
    STRING = "string"
    ID = "id"