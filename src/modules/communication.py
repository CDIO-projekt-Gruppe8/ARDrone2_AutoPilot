# TODO: Implement lift(), land(), move(), set_drone_configuration()

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5556
ip = "xxx.xxx.xx.xx"

# PCMD
# 1: sequence number
# 2: flag (
# 3: roll (drone left-right tilt)
# 4: pitch (drone front-back tilt)
# 5: gaz (drone vertical speed)
# 6: yaw (drone angular speed)
#

lift = "AT*REF=%u,290718208"
land = "AT*REF=%u,290717696"
hover = "AT*PCMD=%u,1,0,0,0,0"
droneUp = "AT*PCMD=%u,1,0,0,1045220557,0"
droneDown = "AT*PCMD=%u,1,0,0,-1102263091,0"
droneForward = "AT*PCMD=%u,1,0,-1102263091,0,0"
droneBack = "AT*PCMD=%u,1,0,1045220557,0,0"
droneLeft = "AT*PCMD=%u,1,-1102263091,0,0,0"
droneRight = "AT*PCMD=%u,1,1045220557,0,0,0"
droneRotLeft = "AT*PCMD=%u,1,0,0,0,-1085485875"
droneRotRight = "AT*PCMD=%u,1,0,0,0,1061997773"
emergencyReset = "AT*REF=<sequence>,290717952"





class Communication(object):
    def test(self):

        pass

    def lift(self):
        sock.sendto(lift, ip, port)

        pass

    def land(self):
        # TODO: Tell the drone to land safely and stand idle
        pass

    def move(self, direction):
        # TODO: Tell the drone to move in given direction
        pass


comm = Communication()
comm.lift()