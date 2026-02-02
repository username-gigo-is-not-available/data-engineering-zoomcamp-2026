from enum import auto, StrEnum


class DatasetType(StrEnum):
    GREEN = auto()
    YELLOW = auto()

    @staticmethod
    def from_str(value: str):
        if value.casefold() == "GREEN".casefold():
            return DatasetType.GREEN
        elif value.casefold() == "YELLOW".casefold():
            return DatasetType.YELLOW
        else:
            raise ValueError(f"Invalid dataset type: {value}")


class FileType(StrEnum):
    CSV = auto()
    PARQUET = auto()

    @property
    def extension(self) -> str:
        return f".{self.value}"


class CompressionType(StrEnum):
    GZ = auto()

    @property
    def extension(self) -> str:
        return f".{self.value}"
