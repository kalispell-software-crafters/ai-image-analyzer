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

# ----------------------------- GENERAL VARIABLES -----------------------------

# Name of the project
project_app_name = "Video and Image Analyzer"


# ----------------------------- PROJECT VARIABLES -----------------------------

# Level of confidence the model should have to report a result
model_confidence_value = 0.45

# Default URL of a Youtube video
video_url = "https://youtu.be/MNn9qKG2UFI"

# Default target item to search for
target_item = "car"

# Default video format
default_video_extension = "mp4"

# Default model type
model_family = "yolov5"

# Model version
model_version = "yolov5s"

# Default type of device, i.e. 'cpu' or 'gpu'
device_type = "cpu"

# Model target class
model_target_class = "person"

# Number of frames to use
total_number_frames = 100
