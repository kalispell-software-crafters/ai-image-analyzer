from fastapi import FastAPI
from src.services.video_service import download_video
from src.services.yolo_service import run_image_analysis

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process_video")
async def process_video(video_url: str, target_item: str):
    download_video(video_url)
    run_image_analysis()
    return {"video_url": video_url, "target_item": target_item }
