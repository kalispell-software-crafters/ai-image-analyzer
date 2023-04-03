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
from typing import Optional, Tuple, Union

import numpy as np
import torch
import ultralytics as ul

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

    def _load_model(self):  # sourcery skip: use-fstring-for-formatting
        """
        Method for loading in the specified model.

        Note
        ----------
        The class object currently accepts only 2 kinds of model families,
        i.e. ``yolov5`` and ``yolov8``.
        """
        # -- Check model family
        accepted_model_family = ["yolov5", "yolov8"]
        if self.model_family not in accepted_model_family:
            msg = ">>> Invalid model family `{}`. Available ones: {}".format(
                self.model_family,
                accepted_model_family,
            )
            logger.error(msg)
            raise ValueError(msg)
        #
        # --- Loading in models
        # YOLOv5
        if self.model_family == "yolov5":
            # URL to use
            model_url = f"ultralytics/{self.model_family}"
            # Check model version
            available_model_versions = torch.hub.list(model_url)
            if self.model_version not in available_model_versions:
                msg = ">> Invalid model version `{}`! Available ones: \n{}"
                msg = msg.format(
                    self.model_version,
                    available_model_versions,
                )
                logger.error(msg)
                raise ValueError(msg)
            #
            # Loading in model
            model = torch.load(
                model_url,
                self.model_version,
                pretrained=True,
            )
        elif self.model_family == "yolov8":
            # Available model versions
            available_model_versions = ["yolov8n.pt", "yolov8n-seg.pt"]
            if self.model_version not in available_model_versions:
                msg = ">> Invalid model version `{}`! Available ones: \n{}"
                msg = msg.format(
                    self.model_version,
                    available_model_versions,
                )
                logger.error(msg)
                raise ValueError(msg)
            #
            # Loading in the model
            model = ul.YOLO(self.model_version)

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

    def predict(
        self,
        image: Union[str, np.ndarray],
        model_confidence: Optional[float] = dv.model_confidence_value,
        size: Optional[Union[Tuple, None]] = None,
    ):
        """
        Method for producing an inference using the specified model.

        Parameters
        -------------
        image : str, numpy.ndarray
            Variable corresponding to the image, for which the inference
            model will do an inference.

        model_confidence : float, optional
            Value corresponding to the model confidence to use when
            performing an inference. This variable must be between
            ``0 < model_confidence <= 1.0``. This variable is set to
            :mod:`~src.utils.default_variables.model_confidence` by default.

        size : NoneType, tuple, optional
            If not ``None``, this variable determines the size of the
            output inference image. This variable is set to ``None``
            by default.

        Returns
        -------------
        image_inference : numpy.ndarray
            Variable corresponding to the inferred
        """
        # --- Checking input parameters
        if not model_confidence or (
            model_confidence <= 0 or model_confidence > 1.0
        ):
            logger.warning(
                f">> Setting confidence to ``{dv.model_confidence_value}"
            )
            model_confidence = dv.model_confidence_value
        # --- Running inference on image

        return
