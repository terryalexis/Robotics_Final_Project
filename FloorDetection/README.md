# Preparation

Download monocular depth mapping model (model-f6b98070.onnx) from https://github.com/isl-org/MiDaS/releases/tag/v2_1
and place it into models/model-f6b98070.onnx

Before running the Floor Finding algorithm, the model must be loaded.  By using
`from find_floor import *` in a given file, the function `loadMonocularDepthModel()` 
should automatically be run.

# Usage
To run the Floor Finding algorithm, provide an image to the find floor function.
It will return the center pixel location of the largest floor section found:
`center = findFloor(img)`

If (0 , 0) is returned, this means the algorithm failed to find a sufficient sized
floor section.  For more sensitivity to small floor areas, lower the `area_threshold`
value near the top of find_floor.py.  (Other thresholds may be tweaked as well such
as the `x_lt_threshold`, `y_gt_threshold`, and `y_lt_threshold` signifying what range of 
gradients the floor sections should produce in an image)

Add an extra parameter True for should_render to render out all the 
intermediate image steps:
`findFloor(img, True)`

# Testing
video_test.py can be run to test the Floor Finding algorithm on a sample
video files or a camera feed.
