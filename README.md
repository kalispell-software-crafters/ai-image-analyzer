# AI Image Analyzer

Sample app to count target items within an image or video.

## Contents

- [Setup](#setup)
- [Resources](#resources)

## Setup

Ensure you have python and pip installed.

```shell
python --version
pip --version
```

From the root directory run the following command to install the dependencies: `pip install -r requirements.txt`

You can run the app using this command: `python -m uvicorn src.api.index:app --reload`

Once running you can navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
