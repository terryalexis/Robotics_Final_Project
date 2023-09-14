# File to test Floor Finding algorithm from video file or feed.

from find_floor import *

video_name = "videos/01Trim4.mp4"

#################
# Process Video #
#################
# Press 'q' on an image window to quit
def processVideo():
  # Webcam or video file
  cap = cv2.VideoCapture(video_name)

  while cap.isOpened():

    # Read in the image
    success, img = cap.read()

    print(findFloor(img, True))

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()

########
# MAIN #
########
processVideo()