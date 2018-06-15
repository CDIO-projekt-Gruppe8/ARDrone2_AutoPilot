import time
from src.interfaces import Commander, Commands
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False

    def explore(self):
        print 'Exploring'
        time.sleep(5)
        while True:
            if self._exploring:
                now = time.clock()
                while time.clock() - now < 10:
                    self.send_command(Commands.RotateRight)
                    time.sleep(1)
                self.send_command(Commands.Up)
                time.sleep(1)

    # Callback must take 1 parameter (bool, indicating if penetrated)
    def penetrate_ring(self, callback, analyzer):
        passed = False
        approached = self.approach_ring(analyzer)
        if not approached:
            if callback is not None:
                callback(passed)
            return
        print 'penetrating'
        self.send_command(Commands.Land)

        self.send_command(Commands.Up)
        # Move forward
        placeholder_int = 1
        while not passed:
            placeholder_int += 1
            self.send_command(Commands.Forward)
            if placeholder_int is 10:
                passed = True
        # Ring is now passed or loop escaped for some reason
        if callback is not None:
            callback(passed)
        pass

    def approach_ring(self, analyzer):
        print 'approaching'
        no_qr_timer = None
        while True:
            time.sleep(1)
            # TODO: Implement. Drone should be directly in front of ring/QR code
            qr_center = analyzer.get_qr_center()
            if qr_center is None:
                if no_qr_timer is None:
                    no_qr_timer = time.clock()
                elif time.clock() - no_qr_timer > 3:
                    return False
                continue
            if abs(qr_center[0]) < 20 and abs(qr_center[1]) < 20:
                if analyzer.get_qr_width() < 100:
                    print analyzer.get_qr_width()
                    now = time.clock()
                    while time.clock() - now < 0.05 or analyzer.get_qr_width() < 100:
                        self.send_command(Commands.Forward)
                    # Centered
                else:
                    print 'approached'
                    return True
            else:
                command = _determine_movement(qr_center)
                direction = next(name for name, value in vars(Commands).items() if value is command)
                print 'Command: ' + str(direction)
                now = time.clock()
                while time.clock() - now < 0.05:
                    self.send_command(command)

    def start(self):
        # TODO: Check if pathfinder-thread is running, create it if not
        self._exploring = True

    def pause(self):
        self._exploring = False

    def stop(self):
        # TODO: Check if pathfinder-thread is running, close if it is
        self._exploring = False


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
