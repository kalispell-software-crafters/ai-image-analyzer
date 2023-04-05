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


# --------------------------- CLASSES AND FUNCTIONS ---------------------------


def main():
    """
    Main function for the Streamlit Application
    """
    data_src = build_page()

    url = get_media_url(data_src)
    target_item = get_target_item()

    handle_analysis(url, target_item)


def build_page():
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

    return data_src


def get_media_url(data_src: str) -> str:
    if data_src == MediaSource.URL:
        return st.sidebar.text_input("URL")
    else:
        return dv.video_url


def get_target_item() -> str:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Search Configuration")
    target_item = st.sidebar.text_input("Item to search for:")
    logger.info(f"Target item to search for: {target_item}")
    return target_item


def handle_analysis(url: str, target_item: str):
    is_valid = validate_input(url, target_item)
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
    prep_service = DataPreparationService(video_obj=video_data)
    model_service = YoloModel()
    analyze_service = AnalyzerService(
        prep_service=prep_service,
        model_service=model_service,
        target_name=target_item,
    )

    height = 0
    width = 0
    # fps = 0
    height_column, width_column = st.columns(2)
    # height_column, width_column, fps_column = st.columns(3)

    with height_column:
        st.markdown("## Height")
        height_text = st.markdown(f"{height}")
    with width_column:
        st.markdown("## Width")
        width_text = st.markdown(f"{width}")
    # with fps_column:
    #     st.markdown("## FPS")
    #     fps_text = st.markdown(f"{fps}")

    st.markdown("---")
    st.markdown("## Frame")
    output = st.empty()

    # TODO Replace temp method with analysis workflow
    # Extract results
    results = analyze_service.run_image_analysis()
    found_target_item_count = Counter()
    for _, frame_results in results.items():
        output.image(frame_results.output_image)
        height_text.markdown(f"{height}")
        width_text.markdown(f"{width}")
        found_target_item_count += Counter(frame_results.inference_results)
        time.sleep(TIME_BETWEEN_FRAMES)

    display_summary(
        target_item=target_item,
        url=url,
        found_target_item_count=found_target_item_count,
    )


def validate_input(url: str, target_item: str):
    if not url:
        st.warning("Please enter a URL for you meida.")
        return False

    if not target_item:
        st.warning("Please enter an item to search for.")
        return False

    return True


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
