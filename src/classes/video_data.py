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

import validators

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

    def download_stream(self):
        """
        Method for downloading the stream from the input video.

        Returns
        ------------
        """

        return
