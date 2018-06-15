import time
from src.interfaces import Commander, Commands
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False

    def explore(self):
        print 'Exploring'
        self.sleep(10)
        while True:
            if self._exploring:
                now = time.clock()
                while time.clock() - now < 2:
                    self.send_command(Commands.RotateRight)
                self.send_command(Commands.Up)
                #self.sleep(1)

    # Callback must take 1 parameter (bool, indicating if penetrated)
    def penetrate_ring(self, callback, analyzer):
        approached = self.approach_ring(analyzer)
        if not approached:
            if callback is not None:
                callback(False)
            return
        print 'penetrating'
        self.send_command(Commands.Land)
        if callback is not None:
            callback(True)
        now = time.clock()
        while time.clock() - now < 0.2:
            self.send_command(Commands.Up)
        # Move forward
        now = time.clock()
        while time.clock() - now < 1:
            self.send_command(Commands.Forward)
        # Ring is now passed or loop escaped for some reason
        if callback is not None:
            callback(True)

    def approach_ring(self, analyzer):
        self.send_command(Commands.Hover)
        time.sleep(1)
        #self.adjust_angle(analyzer)
        print 'approaching'
        no_qr_timer = None
        while True:
            self.sleep(1)
            # TODO: Implement. Drone should be directly in front of ring/QR code
            qr_center = analyzer.get_qr_center()
            if qr_center is None:
                if no_qr_timer is None:
                    print 'Unable to see QR'
                    no_qr_timer = time.clock()
                elif time.clock() - no_qr_timer > 20:
                    return False
                continue
            no_qr_timer = None
            width = analyzer.get_qr_width()
            if abs(qr_center[0]) < 20 and abs(qr_center[1]) < 20 and width >= 100:
                #self.adjust_angle(analyzer)
                print 'approached'
                return True
            elif abs(qr_center[0]) < 100 and abs(qr_center[1]) < 100 and width < 100:
                now = time.clock()
                while time.clock() - now < 0.3 or analyzer.get_qr_width() < 100:
                    self.send_command(Commands.Forward)
                # Centered
            else:
                command = _determine_movement(qr_center)
                direction = next(name for name, value in vars(Commands).items() if value is command)
                print 'Command: ' + str(direction)
                now = time.clock()
                while time.clock() - now < 0.3:
                    self.send_command(command)

    def adjust_angle(self, analyzer):
        print 'adjusting angle'
        width = analyzer.get_qr_width()
        height = analyzer.get_qr_height()
        while height is None or width is None:
            self.sleep(1)
            print 'waiting for qr'
            width = analyzer.get_qr_width()
            height = analyzer.get_qr_height()
        while height/width > 1.2:
            direction = Commands.Left
            width = analyzer.get_qr_width()
            height = analyzer.get_qr_height()
            if height is None or width is None:
                self.sleep(1)
                continue
            init_ratio = height / width
            print 'Move: ' + next(name for name, value in vars(Commands).items() if value is direction)
            self.send_command(direction)
            width = analyzer.get_qr_width()
            height = analyzer.get_qr_height()
            new_ratio = height / width
            if new_ratio > init_ratio:
                direction = Commands.Right
            now = time.clock()
            while time.clock() - now < 0.1:
                self.send_command(direction)
            width = analyzer.get_qr_width()
            height = analyzer.get_qr_height()

    def start(self):
        # TODO: Check if pathfinder-thread is running, create it if not
        self._exploring = True

    def pause(self):
        self._exploring = False

    def stop(self):
        # TODO: Check if pathfinder-thread is running, close if it is
        self._exploring = False

    def sleep(self, seconds):
        time.sleep(seconds)


# Static functions
def _determine_movement(center):
    x = center[0]
    y = center[1]
    if abs(x) > abs(y):
        if center[0] < 0:
            return Commands.Right
        else:
            return Commands.Left
    else:
        if center[1] < 0:
            return Commands.Down
        else:
            return Commands.Up
