import cv2
import numpy as np
from skimage.measure import regionprops
import matplotlib.pyplot as plt

# ROWS = 600
# COLS = 700
ORANGE_RANGE = (1, 16) # range of orange in hsv

def get_center_of_mass(image:np.ndarray):
    """ 
    Get center of mass of orange object in an image

    Parameters:
        image: the image as a numpy array
    Returns:
        x,y coordinates of center of mass of orange object
    """

    # image_resized = cv2.resize(image, (ROWS, COLS))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([ORANGE_RANGE[0], 100, 100])
    upper = np.array([ORANGE_RANGE[1], 255, 255])
    # print(hsv[:,:,2])
    index = 0
    for row in hsv[:,:,2]:
        for col in row:
            pixel = hsv[:,:,2][row][col]
            print(pixel)
            if pixel < 100:
                hsv[:,:,2][row][col] = 100
    # print(hsv[:,:,2])
    plt.imshow(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB))
    mask = cv2.inRange(hsv, lower, upper)
    # plt.imshow(mask)

    kernel = np.ones((7, 7),np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    RGB_img_1 = cv2.cvtColor(dilation, cv2.COLOR_BGR2RGB)
    # plt.imshow(RGB_img_1)
    properties = regionprops(dilation)
    try:
        center_of_mass = properties[0].centroid
    except IndexError:
        print("No orange paper found")
        return (0, 0)

    # Show image and center of mass
    fig, ax = plt.subplots()
    RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ax.imshow(RGB_img)
    ax.scatter(center_of_mass[1], center_of_mass[0], s=160, c='C0', marker='+')
    plt.show()

    return center_of_mass


# Ex:
image_as_numpy_array = cv2.imread("defect-2.png")
get_center_of_mass(image_as_numpy_array)