from src.classes.video_data import VideoData


def download_video(url: str) -> VideoData:
    print(f"Downloading video from the following URL: {url}...")
    return VideoData(url=url, raw_video=[])
