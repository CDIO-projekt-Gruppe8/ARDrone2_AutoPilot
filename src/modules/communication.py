# TODO: Implement lift(), land(), move(), set_drone_configuration()
from src.interfaces import Commands
from src.modules.utils import float_to_bits
import socket

# PCMD
# 1: sequence number
# 2: flag (
# 3: roll (drone left-right tilt)
# 4: pitch (drone front-back tilt)
# 5: gaz (drone vertical speed)
# 6: yaw (drone angular speed)

# Effective control of the drone is reached by sending the AT commands every 30 ms
# A command must be sent at least within 2 s to prevent the drone from thinking the connection is lost


class Communication(object):
    droneLeftSpeed = str(float_to_bits(-0.2))
    droneRightSpeed = str(float_to_bits(0.2))
    dronePosSpeed = str(float_to_bits(0.2))
    droneNegSpeed = str(float_to_bits(-0.2))
    droneRotPosSpeed = str(float_to_bits(0.1))
    droneRotNegSpeed = str(float_to_bits(-0.1))
    # ATCommands
    droneLift = "AT*REF={0},290718208\r\n"
    droneLand = "AT*REF={0},290717696\r\n"
    droneHover = "AT*PCMD={0},1,0,0,0,0\r\n"
    droneUp = "AT*PCMD={0},1,0,0," + dronePosSpeed + ",0\r\n"
    droneDown = "AT*PCMD={0},1,0,0," + droneNegSpeed + ",0\r\n"
    droneBack = "AT*PCMD={0},1,0," + dronePosSpeed + ",0,0\r\n"
    droneForward = "AT*PCMD={0},1,0," + droneNegSpeed + ",0,0\r\n"
    droneLeft = "AT*PCMD={0},1," + droneLeftSpeed + ",0,0,0\r\n"
    droneRight = "AT*PCMD={0},1," + droneRightSpeed + ",0,0,0\r\n"
    droneRotLeft = "AT*PCMD={0},1,0,0,0," + droneRotNegSpeed + "\r\n"
    droneRotRight = "AT*PCMD={0},1,0,0,0," + droneRotPosSpeed + "\r\n"
    emergencyReset = "AT*REF={0},290717952\r\n"
    setMaxAltitude1m = "AT*CONFIG=1,\"control:altitude_max\",\"2000\"\r\n"

    def __init__(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 5556
        self.ip = '192.168.1.1'
        self.sequence_num = 1

    def test(self):
        if self.ip == "192.168.1.1":
            return True, "T1"
        return False, "T2"

    def lift(self):
        print 'Lift'
        self.sockUDP.sendto(self.droneLift.format(self.sequence_num), ('192.168.1.1', 5556))
        self.sequence_num += 1

    def land(self):
        print 'Land'
        self.sockUDP.sendto(self.droneLand.format(self.sequence_num), ('192.168.1.1', 5556))
        self.sequence_num += 1

    def hover(self):
        print 'Hover'
        self.sockUDP.sendto(self.droneHover.format(self.sequence_num), ('192.168.1.1', 5556))
        self.sequence_num += 1

    def set_max_altitude(self):
        self.sockUDP.sendto(self.setMaxAltitude1m.format(self.sequence_num), ('192.168.1.1', 5556))
        self.sequence_num += 1

    def get_nav(self):
        return self.dronePosSpeed

    def move(self, direction):
        if direction is Commands.Hover:
            self.hover()
            return
        if direction is Commands.Land:
            self.land()
            return
        if direction is Commands.Lift:
            self.lift()
            return
        print next(name for name, value in vars(Commands).items() if value is direction)
        if direction is Commands.Up:
            self.sockUDP.sendto(self.droneUp.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.Down:
            self.sockUDP.sendto(self.droneDown.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.Back:
            self.sockUDP.sendto(self.droneBack.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.Forward:
            self.sockUDP.sendto(self.droneForward.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.Left:
            self.sockUDP.sendto(self.droneLeft.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.Right:
            self.sockUDP.sendto(self.droneRight.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.RotateLeft:
            self.sockUDP.sendto(self.droneRotLeft.format(self.sequence_num), (self.ip, self.port))
        elif direction is Commands.RotateRight:
            self.sockUDP.sendto(self.droneRotRight.format(self.sequence_num), (self.ip, self.port))
        self.sequence_num += 1
