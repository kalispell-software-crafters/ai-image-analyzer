from enum import Enum


class MediaSource(str, Enum):
    SAMPLE_DATA = "Sample data"
    URL = "URL of the media"

    def __str__(self) -> str:
        return str.__str__(self)


class MediaType(str, Enum):
    IMAGE = "Image"
    VIDEO = "Video"

    def __str__(self) -> str:
        return str.__str__(self)
