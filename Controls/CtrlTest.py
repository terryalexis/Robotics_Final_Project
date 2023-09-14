#######################################
# Tello Controller Testing Procedures #
#######################################
# sys.path.insert(0, '/FinalProject/Communication/TelloComms')
# import TelloComms as comms
# tello_comms = comms.TelloComms()
# tello_drone = tello_comms.get_tello()
# import Ctrl
# import time
import detect_paper
# from dataclasses import dataclass
from PIL import Image
import numpy
# import threading
# import sys

# ## Test: validating state position update and appropriate dt
# print('Test: validating state position update and appropriate dt ')
# stateThread = threading.Thread(target=Ctrl.getState(), args=(1,))
# stateThread.start()
# # only using default takeoff height for now
# Ctrl.liftOff()
# while 1:
#     tello_comms.take_photo()
#     np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
#     guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
#     Ctrl.search(guide)
# # Using the following getState()
# # def getState():
# #     global x_I, y_I, dt # indicate that I want to use global variables
# #     while 1: # continuously determine
# #         #print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
# #         print(f'v_x: {tello_comms.get_velocity_x()}')
# #         print(f'v_y: {tello_comms.get_velocity_y()}')
# #         x_I = x_I + tello_comms.get_velocity_x()*dt
# #         y_I = y_I + tello_comms.get_velocity_y()*dt
# #         print(f'x_I: {x_I}')
# #         print(f'y_I: {y_I}')
# #         print(f'z: {tello_comms.get_position_z()}')
# # dt = 0.001 worked pretty good

# ## Test: understand threading and get_tello function and try in debug mode
# print('Test: see what get_tello function is, see if threading works, try in debug mode ')
# stateThread = threading.Thread(target=Ctrl.getState, args=())# args=(1,))
# stateThread.start()
# # only using default takeoff height for now
# Ctrl.liftOff()
# tello_drone.land()
# print('have to exit')
# exit()
# # using the following liftOff()
# def liftOff():
#     # unpack
#     global x_I, y_I, dt  # indicate that I want to use global variables
#     desiredHeight = 31  # [cm] Desired height the drone should fly at
#
#     # Confirm where we are at in the global coordinate system
#     print('Position before takeoff:')
#     print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#     fish = tello_comms.get_tello()
#     print(f'this is get_tello function: {fish}')
#
#
#     tello_drone.takeoff()  # drone should go to ~3 ft height
#     # time.sleep(1.5)
#     # bring drone down to ~ 1 ft height to maximize paper visibility in forward camera
#     heightErr = tello_comms.get_position_z() - desiredHeight
#     print(f'heightErr: {heightErr}')
# # note: this is what the get_tello function returns (its used for startup: <djitellopy.tello.Tello object at 0x000001F1A475B3A0>

# ## Test: Understand mid and nonzero sensor positions, try debug mode
# print('Understand mid and nonzero sensor positions, try in debug mode ')
# print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
# fish = tello_comms.tello.get_current_state()['x']
# print(f'x: {fish}')
# fish = tello_comms.tello.get_current_state()['y']
# print(f'x: {fish}')
# stateThread = threading.Thread(target=Ctrl.getState, args=())
# stateThread.start()
# # only using default takeoff height for now
# Ctrl.liftOff()
# tello_drone.land()
# StopNow = 1
# print('have to exit')
# exit()
# ## code used for liftOff
# def liftOff():
#     # unpack
#     global x_I, y_I, dt  # indicate that I want to use global variables
#     desiredHeight = 31  # [cm] Desired height the drone should fly at
#
#     # Confirm where we are at in the global coordinate system
#     print('Position before takeoff:')
#     print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#
#     tello_drone.takeoff()  # drone should go to ~3 ft height
#     # time.sleep(1.5)
#     # bring drone down to ~ 1 ft height to maximize paper visibility in forward camera
#     print(f'z_I: {tello_comms.get_position_z()}')
#     heightErr = tello_comms.get_position_z() - desiredHeight
#     print(f'heightErr: {heightErr}')
#     while abs(heightErr) > 1: # while the drone is not at the desired height...
#         # TODO: IMPLEMENT CONTROLLER THAT ALLOWS YOU TO GET CLOSER TO DESIRED HEIGHT
#         if heightErr > 0: # 0: smallest movement command is 20
#             tello_drone.go_xyz_speed(0,0,heightErr,10) #  move('down', heightErr)
#         else: # if  heightErr < 0:
#             tello_drone.go_xyz_speed(0,0,heightErr,10) # tello_drone.move('up', -heightErr)
#         time.sleep(heightErr/5)  # if needed, wait for drone to move into position
#         print(f'z_I: {tello_comms.get_position_z()}')
#         heightErr = tello_comms.get_position_z() - desiredHeight
#         print(f'heightErr: {heightErr}')
# # notes:
# # mid = -1 = no launch pad
# # think maybe the calibration caused the -100 error on the states, but looks like its
# #     not a big deal since drone still operates ok with it
# # tello_drone.go_xyz_speed(0,0,heightErr,10) still has min distance limitations ->
# #     just use the position function call for height and get as low as you can
# # debug mode works, we just have to make an indicator for the 2nd thread to stop

# ## Test: understand stopping thread and minimum height distance, do i need exit, do i need sleep command')
# print('Test: understand stopping thread and minimum height distance, do i need exit, do i need sleep command')
# print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
# stateThread = threading.Thread(target=Ctrl.getState, args=())
# stateThread.start()
# # only using default takeoff height for now
# Ctrl.liftOff()
# tello_drone.land()
# StopNow = 1
# #print('have to exit')
# exit()
# ## Code for liftOff()
# def liftOff():
#     # unpack
#     global x_I, y_I, dt  # indicate that I want to use global variables
#     desiredHeight = 20  # 31  # [cm] Desired height the drone should fly at. 20 cm ~= 8 in
#
#     # Confirm where we are at in the global coordinate system
#     print('Position before takeoff:')
#     print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#
#     tello_drone.takeoff()  # drone should go to ~3 ft height
#     # bring drone down to maximize paper visibility in forward camera
#     print(f'z_I: {tello_comms.get_position_z()}')
#     heightErr = tello_comms.get_position_z() - desiredHeight
#     print(f'heightErr: {heightErr}')
#     while heightErr > 20: # while the drone is not at the desired height...
#         #if heightErr > 20:  # 0: smallest movement command is 20
#         tello_drone.move('down', heightErr)
#             # no else case, the lower the drone is, the better
#             # else: # if  heightErr < 0:
#             #tello_drone. tello_drone.move('up', -heightErr)
#         #time.sleep(heightErr/5)  # if needed, wait for drone to move into position
#         print(f'z_I: {tello_comms.get_position_z()}')
#         heightErr = tello_comms.get_position_z() - desiredHeight
#         print(f'heightErr: {heightErr}')
#
#     # Confirm where whe are at in the global coordinate system
#     print('Position before searching:')
#     print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
# # Notes:
# # looks like 17 cm is about as low as I can go. keep at 20 cm objective
# #     as a safety buffer against autolanding
# # replay button indicated that the code finished, so exit() not needed
# # sleep command not needed

# print('Test: pivot correctly, see if guide class works')
# guideTest = Ctrl.guide(row = 360, col = 0, depth = 0, foundPaper = 0)
# stateThread = threading.Thread(target=Ctrl.getState, args=())
# stateThread.start()
# Ctrl.liftOff()
# Ctrl.pivot(guideTest)
# tello_drone.land()
# StopNow = 1
# # pivot function before too much change
# # def pivot(guide):
# #     ## unpack
# #     global x_I, y_I, dt  # indicate that I want to use global variables
# #     deltaYaw = calc_pivot_angle(guide)
# #
# #     ## pivot to center on desired location
# #     yawDesired = tello_comms.get_yaw() + deltaYaw
# #     print(f'yawDesired: {yawDesired}')
# #     print(f'deltaYaw: {deltaYaw}')
# #     while abs(deltaYaw) > 1:  # while we are more than 1 degree off from our desired location...
# #         if deltaYaw > 0:
# #             tello_drone.rotate_clockwise(round(deltaYaw))
# #             #time.sleep(deltaYaw / 5) # if needed, wait for drone to move into position
# #             deltaYaw = tello_comms.get_yaw() - yawDesired
# #         else:
# #             tello_drone.rotate_counter_clockwise(round(deltaYaw))
# #             #time.sleep(deltaYaw / 5)  # if needed, wait for drone to move into position
# #             deltaYaw = tello_comms.get_yaw() - yawDesired
# #         if guide.foundPaper:  # if we are going to our found paper, we need to be more accurate, so
# #             guide    = takePic()  # recalculate where the paper is with alexis' algorithm.
# #             deltaYaw = calc_pivot_angle(guide)
# #         print(f'deltaYaw: {deltaYaw}')
# # notes:
# #    Guide class works
# #    tello can recognize -cw = ccw

# print('Test: see if depth traversal works')
# guideTest = Ctrl.guide(row = 360, col = 0, depth = 300, foundPaper = 1)
# stateThread = threading.Thread(target=Ctrl.getState, args=())
# stateThread.start()
# Ctrl.liftOff()
# guideTest = Ctrl.pivot(guideTest)
# Ctrl.move(guideTest)
# tello_drone.land()
# StopNow = 1
## move function before lots of changes
# def move(guide):  # move to desired spot
#     # unpack
#     global x_I, y_I, dt  # indicate that I want to use global variables
#     maxForwardIncrement = 500  # maximum distance tello allows me to go forward
#
#     ## move toward desired location
#     print(f'Current Guide: {guide}')
#     print('Position before moving forward:')
#     print(f'x_I: {x_I}')
#     print(f'y_I: {y_I}')
#     print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#     #guide.depth = 91.44 #assume 3 ft in front for testing
#     # # TODO: FIND DEPTH DISTANCE
#     # # 1: SET STRINGS ON 1, 2, 3, 4, 8 FT DISTANCES
#     # # 2: TURN ON CAMERA AND PLACE ON GLOBAL COORDINATE AND TURN ON VIDEO
#     # # 3: COMMAND TO 1 FT HEIGHT (DO TEST RUN OF TAKING PICTURES TOO)
#     # # 3: Postprocess pixel height ratio to distance
#     # delta_psi = atan(***) * 180 / pi  # [deg] # atan(guide.deltaPw)
#     #           = pixel width difference from center of paper to the center of camera
#     # TODO: make sure im getting depth in cm
#     remainingDepth = guide.depth
#
#     # plan b: use an inverse dynamic velocity controller to go forward to desired location
#     # Calculate desired location in global coordinates
#     x_I_des = x_I + guide.depth*cos(tello_comms.get_yaw())
#     y_I_des = y_I + guide.depth*sin(tello_comms.get_yaw())
#     print(f'x_I_des: {x_I_des}')
#     print(f'y_I_des: {y_I_des}')
#     maxSpeed = 795.73  # [cm / s] max drone speed 17.8 mph
#     maxAngle = 0.4363  # [rad] pitch angle achieved at max speed 25°
#     u        = 10 # 120     # [cm/s] temporarily assume/assign the minimum velocity is the command to give
#     while abs(remainingDepth) > 10:  # while I'm still more than 10 cm from desired location.
#         # Conduct simple fixed point iteration to find the velocity root
#         th = -0.0563 * (maxSpeed-u) / maxAngle  # approximate the pitch angle
#         u = ((x_I_des - x_I) / (cos(tello_comms.get_yaw()) * cos(tello_comms.get_pitch()) * dt))
#                                                         # determine the velocity command [cm/s]
#         print(f'calculated u: {u}')
#         if u < 0:     # if we overshot the location...
#             print(f'u<0')
#             break     # we need to go backwards, not forwards
#         if u > 100: #130:   # If the command says to go faster than walking speed...
#             print('u>130')
#             u = 100 #130   # bring the command down to walking speed to prevent serious
#         elif u < 10:  # If the drone is told to go slower than allowed...
#             print('u<10')
#             u = 10    # set the speed to the minimum speed
#         tello_drone.set_speed(u)  # move forward as much as tello allows in cm/s
#         print('Position after moving forward:')
#         print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#         remainingDepth = norm(array([x_I_des-x_I,y_I_des-y_I]))
#     while abs(remainingDepth) > 1:  # while I'm still more than 1 cm from desired location.
#         print('made it 2 the 2nd while loop!')
#         tello_drone.go_xyz_speed(remainingDepth,0,0,10)  # move forward as much as tello allows in cm/s
#         print('Position after moving forward/backward:')
#         print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
#         remainingDepth = norm(array([x_I_des-x_I,y_I_des-y_I]))




print('Test: detect paper')
# Note: temporarily commenting out
# import TelloComms as comms
# tello_comms = comms.TelloComms()
# tello_drone = tello_comms.get_tello()
# import Ctrl
np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
guide  = detect_paper.get_center_of_mass(np_img, 30) #tello_comms.get_position_z())  # detect a picture



# print('Test: detect paper')
# print(f'This is what is in get_current_state: {tello_comms.get_whole_state()}')
# tello_comms.take_photo()
# np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
# guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
# print(f'guide values when I see the paper on the ground: {guide}')
# tello_comms.take_photo()
# np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
# guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
# print(f'guide values when I see the paper in the handheld air: {guide}')
# np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array
# guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
# print(f'guide values when I dont see paper in the handheld air: {guide}')



# print('Test: Get to paper. detect paper. pivot to paper')
# stateThread = threading.Thread(target=Ctrl.getState, args=())
# stateThread.start()
# guide  = detectPaper.get_center_of_mass(np_img, tello_comms.get_position_z())  # detect a picture
# Ctrl.liftOff()
# tello_comms.take_photo()
# tello_drone.land()
# StopNow = 1
# np_img = numpy.array(Image.open("tello_photo.png")) # convert image to np array

# while 1:
#
#      Ctrl.search(guide)
#





## Teste 3: Try to execute alexis paper finding.





