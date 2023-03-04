from pydantic import BaseModel
from typing import Any

class VideoData(BaseModel):
    raw_video: Any
    url: str
