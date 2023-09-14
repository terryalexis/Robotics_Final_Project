from djitellopy import Tello
import cv2 

TELLO_PHOTO = "tello_photo.png"

class TelloComms():
    def __init__(self):
        self.tello = Tello()
        # in order to be controlled by commands sent over the network,
        # the drone must be placed into SDK mode.
        # SDK mode is set with connect
        self.tello.connect()

    def get_tello(self):
        return self.tello

    def take_photo(self):
        self.tello.streamon()
        frame_read = self.tello.get_frame_read()
        cv2.imwrite(TELLO_PHOTO, frame_read.frame)
        print("*Snap! Photo saved to ", TELLO_PHOTO)
        self.tello.streamoff()

    # note: get_position_x and _y dont work since we dont have
    # their tello landing pad. we have to caluculate x and y
    # ourselfs
    # def get_position_x(self):
    #     self.tello.get_current_state()['x']
    #
    # def get_position_y(self):
    #     return self.tello.get_current_state()['y']

    def get_position_z(self):  # assume floor height = z position
        # return self.tello.get_current_state()['z']
        return self.tello.get_height()

    def get_velocity_x(self):
        return -self.tello.get_current_state()['vgx']
        # looks like the imu is backwards so our real velocity is
        # the negative of what the imu reading is
        # strait infront of camera is x-axis

    def get_velocity_y(self):
        return self.tello.get_current_state()['vgy']
        # left side is y-axis

    def get_velocity_z(self):
        return self.tello.get_current_state()['vgz']
        # up is z-axis

    def get_acceleration_x(self):
        return self.tello.get_current_state()['agx']

    def get_acceleration_y(self):
        return self.tello.get_current_state()['agy']

    def get_acceleration_z(self):
        return self.tello.get_current_state()['agz']

    def get_yaw(self):
        return self.tello.get_current_state()['yaw']

    def get_pitch(self):
        return self.tello.get_current_state()['pitch']

    def get_whole_state(self):
        return self.tello.get_own_udp_object()['state']
