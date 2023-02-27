from pydantic import BaseModel
from src.classes.analysis_results import AnalysisResults

class AnalyzeVideoResponse(BaseModel):
    results: AnalysisResults
    target_item: str
    video_url: str
