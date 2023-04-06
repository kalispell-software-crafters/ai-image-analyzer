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

import logging
from collections import Counter
from typing import Dict, Optional, Union

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from src.classes.analysis_results import AnalysisResults
from src.classes.analyze_video_response import AnalyzeVideoResponse
from src.classes.yolo_model import YoloModel
from src.services.prep_service import DataPreparationService
from src.utils import default_variables as dv

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = ["YoloModel"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class AnalyzerService(object):
    """
    Class object for the main Analysis Service.
    """

    def __init__(
        self,
        prep_service: "DataPreparationService",
        model_service: "YoloModel",
        file_extension: Optional[str] = dv.default_video_extension,
        target_name: Optional[Union[str, list]] = dv.model_target_class,
    ) -> None:
        """
        Class object for the main Analysis Service.
        """
        # --- Instantiate attributes
        self.prep_service = prep_service
        self.model_service = model_service
        self.file_extension = file_extension
        self.target_name = target_name

    def run_image_analysis(self) -> Dict:
        """
        Method for running the image analysis for a given data.
        """
        # --- Extract frames from video
        video_frames_dict = self.prep_service.extraction_of_video_frames(
            file_extension=self.file_extension
        )
        # --- Create inference for each frame
        inference_results = {}
        # Looping over each frame and extracting the results
        with logging_redirect_tqdm(loggers=[logger]):
            tqdm_desc = "Running inference: "
            for frame_idx, frame_metadata in tqdm(
                video_frames_dict.items(), desc=tqdm_desc
            ):
                # Running inference on the image
                (
                    inference_output_image,
                    inference_image_results,
                ) = self.model_service.predict(
                    image=frame_metadata["frame"],
                    target_name=self.target_name,
                )
                # Create object for saving analysis results
                frame_results_obj = AnalysisResults(
                    original_image=frame_metadata["frame"],
                    output_image=inference_output_image,
                    inference_results=inference_image_results,
                )
                # Save results to main dictionary
                inference_results[frame_idx] = frame_results_obj

        return inference_results

    def consolidate_results(
        self,
        inference_results: Dict[int, AnalysisResults],
    ) -> AnalyzeVideoResponse:
        """
        Method for consolidating the output results

        Returns
        ------------
        analyze_video_response : AnalyzeVideoResponse
            Object related to the response of the video analysis.
        """
        # --- Parsing results
        target_items_counts = Counter()
        video_results = [[] for _ in range(len(inference_results))]
        # Looping over each result
        for idx, frame_result in inference_results.items():
            # Saving frame metadata to list
            video_results[idx] = frame_result
            # Calculating counts of target instances
            target_items_counts += Counter(frame_result.inference_results)

        return AnalyzeVideoResponse(
            # results=video_results,
            target_item=list(target_items_counts.keys()),
            video_url=self.prep_service.video_obj.url,
            summary=target_items_counts,
        )
