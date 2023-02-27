from src.services.video_service import download_video

def test_download_video():
    mock_url = "url@youtube.com"

    downloaded_video = download_video(mock_url)

    assert downloaded_video is not None
    assert downloaded_video.url == mock_url
    assert downloaded_video.raw_video == []
