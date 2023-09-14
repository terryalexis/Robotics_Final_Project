#####
# Monocular Depth Mapping code demo found at https://github.com/niconielsen32/ComputerVision/blob/master/monocularDepthAI/monocularDepth.py
# Model from https://github.com/isl-org/MiDaS/releases/tag/v2_1
#####
import numpy as np
import cv2
import time

path_model = "models/"

# The floor plane should have an x_gradient ~ 0 and a y_gradient > 0 
x_lt_threshold = 0.05
y_gt_threshold = 0.25
y_lt_threshold = 0.8

# Minimum area to allow floor find
area_threshold = 25000

##############################
# Load Monocular Depth Model #
##############################
# Load MiDas nueral network model for monocular depth mapping
def loadMonocularDepthModel():
  print("Loading Monocular Depth Model...")
  # Read Network
  model_name = "model-f6b98070.onnx"; # MiDaS v2.1 Large

  # Load the DNN model
  model = cv2.dnn.readNet(path_model + model_name)

  if (model.empty()):
      print("Could not load the neural net! - Check path")
      exit

  # Set backend and target to CUDA to use GPU
  model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
  model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

  return model

#############
# Depth Map #
#############
def depthMap(img, model):
  imgHeight, imgWidth, channels = img.shape
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  # Create Blob from Input Image
  # MiDaS v2.1 Large ( Scale : 1 / 255, Size : 384 x 384, Mean Subtraction : ( 123.675, 116.28, 103.53 ), Channels Order : RGB )
  blob = cv2.dnn.blobFromImage(img, 1/255., (384,384), (123.675, 116.28, 103.53), True, False)

  # Set input to the model
  model.setInput(blob)

  # Make forward pass in model
  depth_map = model.forward()
  
  depth_map = depth_map[0,:,:]
  depth_map = cv2.resize(depth_map, (imgWidth, imgHeight))

  # Normalize the depth_map
  depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

  return depth_map

#############
# Gradients #
#############
# Absolute value shows gradient both ways (values range from 0 to 1)
def gradients(depth_map):
  sobelx64f = cv2.Sobel(depth_map,cv2.CV_64F,1,0,ksize=5)
  sobelx = np.absolute(sobelx64f)
  sobely64f = cv2.Sobel(depth_map,cv2.CV_64F,0,1,ksize=5)
  sobely = np.absolute(sobely64f)
  return sobelx, sobely

###############################
# Find Candidate Floor Pixels #
###############################
def findCandidateFloorPixels(grad_x, grad_y):
  imgHeight, imgWidth = grad_x.shape
  is_floor = np.zeros((imgHeight, imgWidth), np.uint8)

  for i, row in enumerate(grad_x):
    for j, pixel in enumerate(grad_x[0]):
      if grad_x[i][j] < x_lt_threshold and grad_y[i][j] > y_gt_threshold and grad_y[i][j] < y_lt_threshold:
        is_floor[i][j] = 255

  return is_floor

###################
# Threshold Floor #
###################
def thresholdFloor(floor):
  thresh_floor = floor.copy()
  window_size = 12
  threshold = 0.95
  for i in range(0, thresh_floor.shape[0], window_size):
    for j in range(0, thresh_floor.shape[1], window_size):
      if sum(thresh_floor[i:i+window_size, j:j+window_size].flatten()) / (255*window_size*window_size) > threshold:
        thresh_floor[i:i+window_size, j:j+window_size] = 1
      else:
        thresh_floor[i:i+window_size, j:j+window_size] = 0
  ret, thresh = cv2.threshold(thresh_floor,0,255,cv2.THRESH_BINARY)
  return thresh

###################
# Center of Floor #
###################
def centerOfFloor(thresh_floor):
  largest_section = thresh_floor.copy()

  contours, hierarchy = cv2.findContours(largest_section,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  if not contours:
    return (0, 0), largest_section

  blob = max(contours, key=cv2.contourArea)
  #print(cv2.contourArea(blob))

  mask = np.zeros_like(largest_section)
  cv2.fillPoly(mask,[blob],1)

  largest_section = np.multiply(largest_section, mask)

  moments = cv2.moments(blob)
  if cv2.contourArea(blob) > area_threshold and moments["m00"] != 0:
    cX = int(moments["m10"] / moments["m00"])
    cY = int(moments["m01"] / moments["m00"])
  else:
    cX, cY = 0, 0

  return (cX, cY), largest_section

##############
# Find Floor #
##############
# Main function to call into
# Returns center point of largest floor section found in pixel location (x from left, y from top)
# Set should_render to True to see images of each step
#
# Steps:
# 1. Extract depth map
# 2. Calculate x/y gradients
# 3. Find candidate floor pixels
# 4. Threshold floor candidates
# 5. Extract largest floor section
# 6. Find center of largest floor section
def findFloor(img, should_render = False):
      # start time to calculate FPS
      start = time.perf_counter()

      depth_map = depthMap(img, model)
      grad_x, grad_y = gradients(depth_map)
      is_floor = findCandidateFloorPixels(grad_x, grad_y)
      thresh_floor = thresholdFloor(is_floor)
      center, largest_section = centerOfFloor(thresh_floor)

      # End time
      end = time.perf_counter()
      # calculate the FPS for current frame detection
      fps = 1 / (end-start)
      
      if should_render:
        # Show FPS
        #cv2.putText(img, f"{fps:.2f} FPS", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        grad_xy = np.concatenate((grad_x, grad_y), axis=1)
        # cv2.imshow('RGB Image', img) # Image without center crosshair
        cv2.imshow('Depth Map', depth_map)
        cv2.imshow('Gradient x/y', grad_xy)
        cv2.imshow('Floor Candidate Pixels', is_floor)
        cv2.imshow('Floor After Thresholding', thresh_floor)
        cv2.imshow('Largest Section of Floor', largest_section)

        cv2.line(img, (center[0] - 15, center[1]), (center[0] + 15, center[1]), (0, 0, 255), 4)
        cv2.line(img, (center[0], center[1] - 15), (center[0], center[1] + 15), (0, 0, 255), 4)
        cv2.imshow('Center of Floor', img) # Image with center crosshair

      return center

##############
# Load Model #
##############
# Must be performed before running the Find Floor algorithm
model = loadMonocularDepthModel()