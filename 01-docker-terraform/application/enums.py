from enum import Enum, auto, StrEnum


class FileType(StrEnum):
    CSV = auto()
    PARQUET = auto()

    @property
    def extension(self):
        return f".{self.value}"

class TableExistsStrategyType(StrEnum):
    REPLACE = auto()
    APPEND = auto()
    FAIL = auto()
    DELETE_ROWS = auto()