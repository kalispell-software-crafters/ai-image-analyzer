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

import streamlit as st

from src.classes.video_data import VideoData
from src.services.image_analysis_service import run_image_analysis
from src.utils import default_variables as dv
from src.utils.steamlit_enums import MediaSource, MediaType

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = []

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def main():
    """
    Main function for the Streamlit Application
    """
    data_src = build_page()

    url = get_media_url(data_src)

    handle_analysis(url)


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


def handle_analysis(url: str):
    if not url:
        st.warning("Please enter a URL for you meida.")
        return

    st.markdown(f"The target URL is: {url}")

    try:
        video_data = VideoData(url=url)
    except Exception as exception:
        st.warning(
            f"There was a problem processing the URL.\n\nError: {exception}"
        )
        return

    height = 0
    width = 0
    fps = 0
    st1, st2, st3 = st.columns(3)
    with st1:
        st.markdown("## Height")
        st1_text = st.markdown(f"{height}")
    with st2:
        st.markdown("## Width")
        st2_text = st.markdown(f"{width}")
    with st3:
        st.markdown("## FPS")
        st3_text = st.markdown(f"{fps}")

    st.markdown("---")
    output = st.empty()

    # TODO Replace temp method with analysis workflow
    results = run_image_analysis(video_data)
    for frame in results:
        logger.info("Frame results: ", frame)
        output.image(frame.output_image)
        fps = frame.fps
        st1_text.markdown(f"**{height}**")
        st2_text.markdown(f"**{width}**")
        st3_text.markdown(f"**{fps:.2f}**")


if __name__ == "__main__":
    with contextlib.suppress(Exception):
        main()
