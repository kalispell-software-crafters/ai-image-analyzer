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

from src.utils import default_variables as dv

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = []

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

# ------------------------- ENVIRONMENT VARIABLES -----------------------------


# ------------------------------ MAIN FUNCTIONS -------------------------------


def main():
    """
    Main function for the Streamlit Application
    """
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
    #
    st.sidebar.markdown("---")
    # -- Media-specific
    st.sidebar.subheader("Media configuration")
    # Type of media to use, i.e. video or image
    input_data_type = st.sidebar.radio(
        "Select input type: ",
        ["image", "video"],
    )
    # Input source, i.e. sample data, local, or on the web.
    data_src = st.sidebar.radio(
        "Select input source: ",
        [
            "Sample data",
            "URL of the media",
            "Upload your own data",
        ],
    )
    logger.info(f"{data_src} | {input_data_type} | {confidence}")

    return


if __name__ == "__main__":
    with contextlib.suppress(Exception):
        main()
