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
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional

import cv2
import numpy as np

from src.classes.video_data import VideoData
from src.utils import default_variables as dv

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = ["DataPreparationService"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class DataPreparationService(object):
    """
    Main class object for the 'Data Preparation Service'.
    """

    def __init__(self, video_obj: "VideoData") -> None:
        """
        Class object for the 'Data Preparation Service'.

        Parameters
        -------------
        video_obj : ``VideData``
            Object for downloading the video.
        """
        # --- Initializing attributes
        self.video_obj = video_obj

    def show_params(self):
        """
        Method to show the attributes of the class.
        """
        msg = "-" * 50 + "\n"
        msg += "\t---- INPUT PARAMETERS ----" + "\n"
        msg += "" + "\n"
        # Keys to omit
        columns_to_omit = []
        # Sorting keys of dictionary
        keys_sorted = np.sort(list(self.__dict__.keys()))
        for key_ii in keys_sorted:
            if key_ii not in columns_to_omit:
                msg += f"\t>>> {key_ii} : {self.__dict__[key_ii]}\n"
        #
        msg += "\n" + "-" * 50 + "\n"
        logger.info(msg)

    def extraction_of_video_frames(
        self,
        file_extension: Optional[str] = dv.default_video_extension,
    ) -> Dict:
        """
        Method for extracting and storing the frames of the video.
        """
        # --- Download the video and extracting frames
        # -- Video download
        video_local_filepath = self.video_obj.download_stream(
            file_extension=file_extension,
        )
        if not Path(video_local_filepath).exists():
            msg = f">>> Filepath `{video_local_filepath}` does not exist!!"
            logger.error(msg)
            raise FileNotFoundError(msg)
        # -- Extract frames
        # - Open file and read in the frames
        video_cv = cv2.VideoCapture(video_local_filepath)
        # - Extracting video metadata
        width = int(video_cv.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_cv.get(cv2.CAP_PROP_FRAME_HEIGHT))
        number_frames = int(video_cv.get(cv2.CAP_PROP_FRAME_COUNT))

        logger.info(
            f"Video -> width: {width} | height: {height} | N: {number_frames}"
        )
        # - Looping over each frame
        video_frames_dict = defaultdict(dict)
        frame_idx = 0
        start_time = time.time()
        while True:
            # Extracting frame
            ret, frame = video_cv.read()
            if ret % 10 == 0:
                logger.info(f"ret: {ret}")
            if not ret or frame_idx == 500:
                break
            # Saving frame metadata to dictionary
            video_frames_dict[frame_idx] = {"frame": frame}
            # Increasing frame index
            frame_idx += 1
        #
        end_time = time.time()
        logger.info(f">> Took: {end_time - start_time}")
        # Releasing video object
        video_cv.release()

        return video_frames_dict


if __name__ == "__main__":
    # Initializing video object
    video_obj = VideoData(url=dv.video_url)
    # Sending it to the Data Preparation object
    data_prep_obj = DataPreparationService(video_obj=video_obj)
    data_prep_obj.show_params()
