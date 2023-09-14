##############################
# Team PASE Tello controller #
##############################
# Notes: in the main algorithm, teammates will only need to call liftOff, search, and takePic

import TelloComms as comms
import time
from math import cos, sin, tan
from numpy import array
from numpy.linalg import norm
import detectPaper
from dataclasses import dataclass
import numpy
from PIL import Image

tello_comms = comms.TelloComms()
tello_drone = tello_comms.get_tello()

# Define states
x_I = 0
y_I = 0 # u, z_I, and yaw can be measured directly so they won't needed

# Define time step
dt  = 0.001 # [s] assumption based on testing ***************************8might need to changes

# Defining end boolean for 2nd getState thread
StopNow = 0;

@dataclass
class guide: # guide: class with pixel location and depth the team wants drone to fly to.
  row: int         # pixel row that the desired location is at
  col: int         # pixel column that the desired location is at
  depth: float     # picture's distance [cm] that the drone needs to fly to
  foundPaper: int  # 1 or 0 boolean indicating that drone should land after flying to desired location


def takePic():
    tello_comms.take_photo()
    np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
    guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
    return guide


def getState():
    global x_I, y_I, dt, StopNow # indicate that I want to use global variables
    while 1:  # continuously determine state
        x_I = x_I + tello_comms.get_velocity_x()*dt
        y_I = y_I + tello_comms.get_velocity_y()*dt
        # print(f'x_I: {x_I}')
        # print(f'y_I: {y_I}')
        # print(f'z: {tello_comms.get_position_z()}')
        if StopNow:
            break


def liftOff():
    # unpack
    global x_I, y_I, dt  # indicate that I want to use global variables
    desiredHeight = 20  # [cm] Desired height the drone should fly at. 20 cm ~= 8 in

    # # Debug: Confirm where we are at in the global coordinate system
    # print('Position before takeoff:')
    # print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')

    tello_drone.takeoff()  # drone should go to ~3 ft height
    # Bring drone down to maximize paper visibility in forward camera
    # print(f'z_I: {tello_comms.get_position_z()}')
    heightErr = tello_comms.get_position_z() - desiredHeight
    # print(f'heightErr: {heightErr}')
    while heightErr > 20: # while the drone is not at the desired height...
        tello_drone.move('down', heightErr)
        # print(f'z_I: {tello_comms.get_position_z()}')
        heightErr = tello_comms.get_position_z() - desiredHeight
        # print(f'heightErr: {heightErr}')
        # exact height is not critical

    # Confirm where we are at in the global coordinate system
    print('Position before searching:')
    print(f'x_I: {x_I}')
    print(f'y_I: {y_I}')
    print(f'z_I: {tello_comms.get_position_z()}')
    print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')


def calc_pivot_angle(guide): # calculate deltayaw angle
    # image size we are using: 960x720
    FOV        = 55.024 # [deg] ~ 0.9604 rad
    maxCol     = 960
    midCol     = maxCol/2
    deltaPixel = guide.col - midCol # number of pixels desired location is from center
    deltaYaw   = deltaPixel/maxCol*FOV  # [deg]
    return deltaYaw


def pivot(guide):
    ## unpack
    global x_I, y_I, dt  # indicate that I want to use global variables
    deltaYaw = calc_pivot_angle(guide)

    ## pivot to center on desired location
    yawDesired = tello_comms.get_yaw() + deltaYaw
    # print(f'yawDesired: {yawDesired}')
    # print(f'deltaYaw: {deltaYaw}')
    while abs(deltaYaw) > 1:  # while we are more than 1 degree off from our desired location...
        tello_drone.rotate_clockwise(round(deltaYaw))
        deltaYaw = tello_comms.get_yaw() - yawDesired
        if guide.foundPaper:  # if we are going to our found paper, we need to be more accurate, so
            guide.row = 360
            guide.col = 480
            guide.depth = 91.44
            guide.foundPaper = 1 #debugging test
                         #takePic()  # recalculate where the paper is with alexis' algorithm.
            deltaYaw = calc_pivot_angle(guide)
        print(f'current yaw: {tello_comms.get_yaw()}')
        print(f'yaw Desired: {yawDesired}')
        print(f'deltaYaw: {deltaYaw}')

    ## Confirm where we are at in the global coordinate system
    print('Position before traveling depth:')
    print(f'x_I: {x_I}')
    print(f'y_I: {y_I}')
    print(f'z_I: {tello_comms.get_position_z()}')
    print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
    return guide


# def planA(): # just command to go forward to that desired location
    # while abs(remainingDepth) > 1: # while I'm still more than 1 cm from desired location.
    #     if remainingDepth > maxForwardIncrement:
    #         tello_drone.move('forward', maxForwardIncrement) # move forward as much as tello allows
    #         x_I = tello_comms.get_position_x()
    #         y_I = tello_comms.get_position_y()
    #         psi_I = tello_comms.get_position_psi()
    #         remainingDepth = remainingDepth - maxForwardIncrement
    #     else:
    #         if remainingDepth > 0:
    #             tello_drone.move('forward', remainingDepth)  # move forward remaining distance
    #         else:
    #             tello_drone.move('backward', -remainingDepth)  # move backward remaining distance
    #         remainingDepth = 0
    #     x_I = tello_comms.get_position_x()
    #     y_I = tello_comms.get_position_y()
    #     psi_I = tello_comms.get_position_psi()
    #     print('Position after moving forward/backward:')
    #     print(f'x_I = {x_I}')
    #     print(f'y_I = {y_I}')
    #     print(f'z_I = {z_I}')
    #     print(f'psi_I = {psi_I}')


def move(guide):  # move to desired spot
    # unpack
    global x_I, y_I, dt  # indicate that I want to use global variables
    maxForwardIncrement = 500  # maximum distance tello allows me to go forward

    ## move toward desired location
    print(f'Current Guide: {guide}')
    print('Position before moving forward:')
    print(f'x_I: {x_I}')
    print(f'y_I: {y_I}')
    print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
    #guide.depth = 91.44 #assume 3 ft in front for testing
    # # TODO: FIND DEPTH DISTANCE
    # # 1: SET STRINGS ON 1, 2, 3, 4, 8 FT DISTANCES
    # # 2: TURN ON CAMERA AND PLACE ON GLOBAL COORDINATE AND TURN ON VIDEO
    # # 3: COMMAND TO 1 FT HEIGHT (DO TEST RUN OF TAKING PICTURES TOO)
    # # 3: Postprocess pixel height ratio to distance
    # delta_psi = atan(***) * 180 / pi  # [deg] # atan(guide.deltaPw)
    #           = pixel width difference from center of paper to the center of camera
    # TODO: make sure im getting depth in cm
    remainingDepth = guide.depth

    # plan b: use an inverse dynamic velocity controller to go forward to desired location
    # Calculate desired location in global coordinates
    x_I_des = x_I + guide.depth*cos(tello_comms.get_yaw())
    y_I_des = y_I + guide.depth*sin(tello_comms.get_yaw())
    print(f'x_I_des: {x_I_des}')
    print(f'y_I_des: {y_I_des}')
    maxSpeed = 795.73  # [cm / s] max drone speed 17.8 mph
    maxAngle = 0.4363  # [rad] pitch angle achieved at max speed 25°
    u        = 10 # 120     # [cm/s] temporarily assume/assign the minimum velocity is the command to give
    while abs(remainingDepth) > 10:  # while I'm still more than 10 cm from desired location.
        # Conduct simple fixed point iteration to find the velocity root
        th = -0.0563 * (maxSpeed-u) / maxAngle  # approximate the pitch angle
        u = ((x_I_des - x_I) / (cos(tello_comms.get_yaw()) * cos(tello_comms.get_pitch()) * dt))
                                                        # determine the velocity command [cm/s]
        print(f'calculated u: {u}')
        if u < 0:     # if we overshot the location...
            print(f'u<0')
            break     # we need to go backwards, not forwards
        if u > 50:  #100: #130:   # If the command says to go faster than walking speed...
            #print('u>100')
            print('u>50')
            u = 50 #130   # bring the command down to walking speed to prevent serious
        elif u < 10:  # If the drone is told to go slower than allowed...
            print('u<10')
            u = 10    # set the speed to the minimum speed
        tello_drone.set_speed(u)  # move forward as much as tello allows in cm/s
        print('Position after moving forward:')
        print(f'x_I: {x_I}')
        print(f'y_I: {y_I}')
        print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
        remainingDepth = norm(array([x_I_des-x_I,y_I_des-y_I]))
    #***********************88start here
    while abs(remainingDepth) > 1:  # while I'm still more than 1 cm from desired location.
        print('made it 2 the 2nd while loop!')
        tello_drone.move('forward', 20)
        tello_drone.go_xyz_speed(round(remainingDepth),0,0,10)  # move forward as much as tello allows in cm/s
        print('Position after moving forward/backward:')
        print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
        remainingDepth = norm(array([x_I_des-x_I,y_I_des-y_I]))


def search(guide):
    guide = pivot(guide)
    move(guide)
    if guide.foundPaper:
        tello_drone.land()
        StopNow = 1
        tello_drone.end()
        quit()
