# TODO: Implement lift(), land(), move(), set_drone_configuration()
from interfaces import Direction
import socket

# PCMD
# 1: sequence number
# 2: flag (
# 3: roll (drone left-right tilt)
# 4: pitch (drone front-back tilt)
# 5: gaz (drone vertical speed)
# 6: yaw (drone angular speed)
#


class Communication(object):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 5556
    ip = "xxx.xxx.xx.xx"

    sequence_num = 1

    # ATCommands
    droneLift = "AT*REF={0},290718208"
    droneLand = "AT*REF={0},290717696"
    droneHover = "AT*PCMD={0},1,0,0,0,0"
    droneUp = "AT*PCMD={0},1,0,0,1045220557,0"
    droneDown = "AT*PCMD={0},1,0,0,-1102263091,0"
    droneForward = "AT*PCMD={0},1,0,-1102263091,0,0"
    droneBack = "AT*PCMD={0},1,0,1045220557,0,0"
    droneLeft = "AT*PCMD={0},1,-1102263091,0,0,0"
    droneRight = "AT*PCMD={0},1,1045220557,0,0,0"
    droneRotLeft = "AT*PCMD={0},1,0,0,0,-1085485875"
    droneRotRight = "AT*PCMD={0},1,0,0,0,1061997773"
    emergencyReset = "AT*REF={0},290717952"

    def test(self):
        pass

    def lift(self):
        self.sock.sendto(self.droneLift.format(self.sequence_num), self.ip, self.port)
        self.sequence_num += 1

    def land(self):
        self.sock.sendto(self.droneLand.format(self.sequence_num), self.ip, self.port)
        self.sequence_num += 1

    def move(self, direction):
        if direction is Direction.Up:
            self.sock.sendto(self.droneUp.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.Down:
            self.sock.sendto(self.droneDown.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.Back:
            self.sock.sendto(self.droneBack.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.Forward:
            self.sock.sendto(self.droneForward.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.Left:
            self.sock.sendto(self.droneLeft.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.Right:
            self.sock.sendto(self.droneRight.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.RotateLeft:
            self.sock.sendto(self.droneRotLeft.format(self.sequence_num), self.ip, self.port)
        elif direction is Direction.RotateRight:
            self.sock.sendto(self.droneRotRight.format(self.sequence_num), self.ip, self.port)
        self.sequence_num += 1


#comm = Communication()
#comm.lift()

