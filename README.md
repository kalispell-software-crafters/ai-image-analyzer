# AI Image Analyzer

Sample app to count target items within an image or video.

## Contents

- [Setup](#setup)
- [Tests](#tests)
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

## Tests

Unit tests can be found under the `src` folder alongside source code. Test files end with `_test`. The following command will run all of the tests.

```shell
python -m pytest -v -s
```

The `-v` argument is for verbose output. The `-s` argument is for turning off the capture mode so that print statements are printed to the console.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/en/7.2.x/)
