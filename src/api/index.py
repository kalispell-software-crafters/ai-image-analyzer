from fastapi import FastAPI
from src.classes.analyze_video_response import AnalyzeVideoResponse
from src.services.image_analysis_service import run_image_analysis
from src.services.video_service import download_video

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze_video")
async def analyze_video(video_url: str, target_item: str) -> AnalyzeVideoResponse:
    video_data = download_video(video_url)
    results = run_image_analysis(video_data)
    return AnalyzeVideoResponse(video_url=video_url, target_item=target_item, results=results)
