from src.classes.video_data import VideoData
from src.services.image_analysis_service import run_image_analysis


def test_run_image_analysis():
    mock_video_data = VideoData(url="url@youtube.com", raw_video=[])

    results = run_image_analysis(mock_video_data)

    assert results is not None
