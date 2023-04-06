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

from __future__ import absolute_import

import contextlib
import logging
import time
from collections import Counter
from typing import Tuple

import pandas as pd
import streamlit as st

from src.classes.video_data import VideoData
from src.classes.yolo_model import YoloModel
from src.services.image_analysis_service import AnalyzerService
from src.services.prep_service import DataPreparationService
from src.utils import default_variables as dv
from src.utils.steamlit_enums import MediaSource, MediaType

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = []

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# --------------------------- ENVIRONMENT VARIABLES ---------------------------

# Amount of time (in seconds) to sleep between frames
TIME_BETWEEN_FRAMES = 0.01

# Time for inference
TIME_FORM_INFERENCE_PER_FRAME = 1e-2

# --------------------------- CLASSES AND FUNCTIONS ---------------------------


def main():
    """
    Main function for the Streamlit Application
    """
    # --- Defining layout
    data_src, model_selection, number_frames = build_page()
    # --- Defining Yolo Model
    model_service = load_model_service(model_selection=model_selection)

    url = get_media_url(data_src)
    target_item = get_target_item(model_service=model_service)

    handle_analysis(
        url,
        target_item,
        model_selection,
        number_frames,
        model_selection,
    )


def build_page() -> Tuple[str, str]:
    # --- Defining the layout
    st.set_page_config(page_title=dv.project_app_name)
    # - Main page
    st.title(dv.project_app_name)

    # - Sidebar of the application
    st.sidebar.title("Settings")
    # -- Model-specific configuration
    st.sidebar.subheader("Model configuration")
    # - Confidence level to use
    confidence = st.sidebar.slider(
        "Confidence level of the model",
        min_value=0.1,
        max_value=1.0,
        value=dv.model_confidence_value,
    )
    # Type of model to use
    model_selection = st.sidebar.radio(
        "Select type of model:", ["yolov5", "yolov8"]
    )
    # Number of frames to use
    number_frames = st.sidebar.slider(
        label="Pick number of frames to analyze",
        min_value=10,
        max_value=1000,
        value=dv.total_number_frames,
    )
    # Type of device to use, i.e. CPU or GPU
    st.sidebar.markdown("---")
    # -- Media-specific
    st.sidebar.subheader("Media configuration")

    # Type of media to use, i.e. video or image
    input_data_type = st.sidebar.radio(
        "Select media type: ",
        [MediaType.VIDEO],
    )
    # Input source, i.e. sample data, local, or on the web.
    data_src = st.sidebar.radio(
        "Select media source: ",
        [
            MediaSource.SAMPLE_DATA,
            MediaSource.URL,
        ],
    )

    logger.info(f"Data Source: {data_src}")
    logger.info(f"Type: {input_data_type}")
    logger.info(f"Confidence: {confidence}")

    return data_src, model_selection, number_frames


def get_media_url(data_src: str) -> str:
    if data_src == MediaSource.URL:
        return st.sidebar.text_input("URL")
    else:
        return dv.video_url


def get_target_item(model_service: "YoloModel") -> str:
    """
    Function to get the target item to query.

    Parameters
    ---------------
    model_selection : str
        Type of model to use.

    model_service : ``YoloModel``
        Service used for evaluating the model

    Returns
    ----------
    target_item : str
        Name of the target items to use.
    """
    # -- Extracting set of possible classes
    class_names = model_service.class_names

    return (
        st.sidebar.multiselect(
            "Select Classes", class_names, default=[class_names[0]]
        )
        if st.sidebar.checkbox("Custom Classes")
        else None
    )


def handle_analysis(
    url: str,
    target_item: str,
    model_selection: str,
    number_frames: int,
    model_service: "YoloModel",
):
    """
    Function that handles the overall execution of the Streamlit app.

    Parameters
    -------------
    url : str
        URL of the Video to YouTube analyze.

    target_item : str, NoneType, optional
    """
    is_valid = validate_input(url)
    if not is_valid:
        return

    try:
        video_data = VideoData(url=url)
    except Exception as exception:
        st.warning(
            f"There was a problem processing the URL.\n\nError: {exception}"
        )
        return
    #
    # --- Initializing service
    # Initializing services
    prep_service = DataPreparationService(
        video_obj=video_data,
        number_frames=number_frames,
    )
    model_service = load_model_service(model_selection=model_selection)
    analyze_service = AnalyzerService(
        prep_service=prep_service,
        model_service=model_service,
        target_name=target_item,
    )

    height = 0
    width = 0
    height_column, width_column = st.columns(2)

    with height_column:
        st.markdown("## Height")
        height_text = st.markdown(f"{height}")
    with width_column:
        st.markdown("## Width")
        width_text = st.markdown(f"{width}")

    st.markdown("---")
    st.markdown("## Frame")
    output = st.empty()

    # Time to wait to run
    time_per_inference = TIME_FORM_INFERENCE_PER_FRAME * number_frames
    # Extract results
    with st.spinner(text="Calculating inferences ..."):
        results = analyze_service.run_image_analysis()
        time.sleep(time_per_inference)
    #
    # Showing results
    found_target_item_count = Counter()
    for _, frame_results in results.items():
        output.image(frame_results.output_image)
        height_text.markdown(f"{frame_results.output_image.height}")
        width_text.markdown(f"{frame_results.output_image.width}")
        found_target_item_count += Counter(frame_results.inference_results)
        time.sleep(TIME_BETWEEN_FRAMES)

    display_summary(
        target_item=target_item,
        url=url,
        found_target_item_count=found_target_item_count,
    )


def validate_input(url: str):
    if not url:
        st.warning("Please enter a URL for you meida.")
        return False

    return True


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


def display_summary(
    target_item: str,
    url: str,
    found_target_item_count: "Counter",
):
    st.markdown("---")
    st.markdown("## Results Summary")
    st.markdown(f"The target URL is: {url}")
    st.markdown(f"The target item is: {target_item}")
    # -- Create DataFrame from input dictionary
    found_target_item_df = (
        pd.DataFrame.from_dict(found_target_item_count, orient="index")
        .reset_index()
        .rename(columns={0: "Counts", "index": "Class Names"})
    )
    st.dataframe(found_target_item_df)


if __name__ == "__main__":
    with contextlib.suppress(Exception):
        main()
