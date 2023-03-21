# MIT License
#
# Copyright (c) 2023 Victor Calderon and Travis Craft
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from fastapi import FastAPI, HTTPException

from src.classes.analyze_video_response import AnalyzeVideoResponse
from src.services.image_analysis_service import run_image_analysis
from src.services.video_service import download_video

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze_video")
async def analyze_video(
    video_url: str, target_item: str
) -> AnalyzeVideoResponse:
    try:
        video_data = download_video(video_url)
        results = run_image_analysis(video_data)
        return AnalyzeVideoResponse(
            video_url=video_url, target_item=target_item, results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
