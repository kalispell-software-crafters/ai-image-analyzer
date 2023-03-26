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
import tempfile
from pathlib import Path
from typing import Optional, Union

import pytube as pt
import validators

from src.utils import default_variables as dv

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = ["VideoData"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class VideoData(object):
    """
    Class object for interacting with an input video
    """

    def __init__(self, url: str):
        """
        Class object that interacts with video files.
        """
        # -- Defining class attributes
        self.url = url
        # Validating URL
        self._validate_video_url()

    def _validate_video_url(self):
        """
        Method for validating the input URL. This method checks
        whether or not the URL is a valid Youtube URL.

        Raises
        ----------
        ValueError : Exception
            This error gets raised whenever the URL is not valid.
        """
        # Validating the input URL
        if not validators.url(self.url):
            msg = f">>> URL `{self.url}` is not valid!"
            logger.error(msg)
            raise ValueError(msg)

    def download_stream(
        self,
        file_extension: Optional[str] = dv.default_video_extension,
        output_path: Optional[Union[str, None]] = None,
        output_basename: Optional[str] = "output_video",
    ) -> str:
        """
        Method for downloading the stream from the input video.

        Parameters
        --------------
        file_extension : str, optional
            Extension to use for the video stream. This variable is set to
            :mod:`~src.utils.default_variables.default_video_extension` as
            default.

        output_path : str, NoneType, optional
            Path to the output directory, to which the output file will be
            saved. If ``None``, a temporary directory will be created.
            This variable is set to ``None`` by default.

        output_basename : str, optional
            Basename of the output video. This variable is set to
            ``output_video`` by default.

        Returns
        ------------
        output_filepath : str
            Path to the output video file.
        """
        # --- Downloading video from URL
        # -- Initialize object
        video_obj = pt.YouTube(url=self.url)
        # -- Filter for the specified video format, e.g. 'mp4'
        # Making sure that there are
        video_streams = video_obj.streams.filter(file_extension=file_extension)
        # Check that there are available streams
        if not video_streams:
            msg = (
                f">>> No '{file_extension}' streams available for {self.url}!"
            )
            logger.error(msg)
            raise TypeError(msg)
        #
        logger.info(
            f">> There are '{len(video_streams)}' streams for the video"
        )
        # --- Download the video object
        # Check the output directory
        if not output_path:
            # Creating new temporary directory
            output_path = str(
                Path("/tmp").joinpath(
                    Path(tempfile.NamedTemporaryFile().name).name
                )
            )
            Path(output_path).mkdir(parents=True, exist_ok=True)
            logger.warning(">>> Temporary output directory created!")
            #
        logger.info(f">>> Output path: {output_path}")

        # Downloading video object
        return video_streams.first().download(
            output_path=output_path,
            filename=f"{output_basename}.{file_extension}",
            skip_existing=False,
        )
