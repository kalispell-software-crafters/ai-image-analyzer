from typing import Any

from pydantic import BaseModel


class VideoData(BaseModel):
    raw_video: Any
    url: str
