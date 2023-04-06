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

from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException

from src.classes.analyze_video_response import AnalyzeVideoResponse
from src.classes.video_data import VideoData
from src.classes.yolo_model import YoloModel
from src.services.image_analysis_service import AnalyzerService
from src.services.prep_service import DataPreparationService
from src.utils import default_variables as dv
from src.utils.default_variables import target_item, video_url

app = FastAPI()


class ModelChoices(str, Enum):
    yolov5 = "yolov5"
    yolov8 = "yolov8"


def get_model_attributes(model_selection: str):
    """
    Function to determine the type of model family and
    model version to use

    Parameters
    -------------
    model_selection : str
        Type of model to use. Options: [`yolov5`, `yolov8`]

    Returns
    -----------
    model_config : dict
        Dictionary containing the set of configuration to
        use for the specified model.
    """
    if model_selection == "yolov5":
        return {"model_family": "yolov5", "model_version": "yolov5s"}
    elif model_selection == "yolov8":
        return {"model_family": "yolov8", "model_version": "yolov8n.pt"}


def load_model_service(model_selection: str) -> "YoloModel":
    """
    Function to load the ``model`` service.

    Parameters
    -------------
    model_selection : str
        Type of model to use. Options: [`yolov5`, `yolov8`]

    Returns
    ----------
    model_service : ``src.classes.yolo_model.YoloModel``
        Service corresponding to the initialized Yolo Model
    """
    # -- Extracting set of possible classes
    model_config_dict = get_model_attributes(model_selection=model_selection)

    return YoloModel(
        model_family=model_config_dict["model_family"],
        model_version=model_config_dict["model_version"],
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze_video2")
async def analyze_video(
    video_url: Optional[str] = video_url,
    number_of_frames: Optional[int] = dv.total_number_frames,
    target_item: Optional[str] = target_item,
    model_selection: ModelChoices = ModelChoices.yolov5,
) -> AnalyzeVideoResponse:
    try:
        # --- Setting up services
        video_data = VideoData(url=video_url)
        prep_service = DataPreparationService(
            video_obj=video_data,
            number_frames=number_of_frames,
        )
        model_service = load_model_service(
            model_selection=model_selection.value
        )
        analyze_service = AnalyzerService(
            prep_service=prep_service,
            model_service=model_service,
            target_name=target_item,
        )
        # --- Running inference
        analysis_results = analyze_service.run_image_analysis()

        return analyze_service.consolidate_results(
            inference_results=analysis_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
