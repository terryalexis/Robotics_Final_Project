import TelloComms as comms
import time

tello_comms = comms.TelloComms()
tello_drone = tello_comms.get_tello()


tello_drone.takeoff()
tello_comms.take_photo()
print("X ", tello_comms.get_acceleration_x())
print("Y ", tello_comms.get_acceleration_y())
print("Z ", tello_comms.get_acceleration_z())
print("vX ", tello_comms.get_velocity_x())
print("vY ", tello_comms.get_velocity_y())
print("vZ ", tello_comms.get_velocity_z())
tello_drone.land()

