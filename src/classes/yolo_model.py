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
from typing import Optional, Union

import numpy as np
import torch

from src.utils import default_variables as dv

__author__ = ["Victor Calderon and Travis Craft"]
__maintainer__ = ["Victor Calderon and Travis Craft"]
__all__ = ["YoloModel"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


class YoloModel(object):
    """
    Class object for the object identification ``YOLO`` model algorithm.
    """

    def __init__(
        self,
        model_family: Optional[str] = dv.model_family,
        model_version: Optional[str] = dv.model_version,
        device: Optional[Union[str, None]] = None,
    ) -> None:
        """
        Class object for the ``YOLO`` model algorithm.

        Parameters
        -------------
        model_type : str
            Type of model to use, e.g. ``yolo5``.
        """
        # --- Initializing class attributes
        self.model_family = model_family
        self.model_version = model_version
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.model = self._load_model()
        self.model_classes = self._get_model_classes()

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

    def _load_model(self):
        """
        Method for loading in the specified model.
        """
        # Downloading model
        model = torch.hub.load(
            f"ultralytics/{self.model_family}",
            self.model_version,
            pretrained=True,
        )
        # Sending model to device
        model.to(self.device)

        return model

    def _get_model_classes(self):
        """
        Method for extracting the model classes.

        Returns
        -----------
        model_classes : list
            List of classes and the corresponding indices
        """

        return list(self.model.names.keys())
