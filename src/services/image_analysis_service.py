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

from typing import List

from src.classes.analysis_results import (
    AnalysisResults,
    DetectedObject,
    InferenceResults,
)
from src.classes.video_data import VideoData


def run_image_analysis(video_data: VideoData) -> List[AnalysisResults]:
    """
    Method for analyzing video data using a modeling service.

    Parameters
    --------------
    video_data : VideoData
        Video data to be analyzed.

    Returns
    ------------
    analysis_results : List[AnalysisResults]
        List of AnalysisResults objects for each frame.
        This includes the processed image and inference results
        from the modeling service.

    """
    print("Running image analysis...")
    return [
        AnalysisResults(
            output_image={},
            fps=60,
            inference_results=InferenceResults(
                detected_objects=[
                    DetectedObject(name="car"),
                    DetectedObject(name="tree"),
                ]
            ),
        )
    ]
