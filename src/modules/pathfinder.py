import time
from src.interfaces import Commander, Commands
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False

    def explore(self):
        print 'Exploring'
        while True:
            time.sleep(1)
            if self._exploring:
                for i in range(0, 4):
                    self.send_command(Commands.RotateRight)
                time.sleep(1)
                self.send_command(Commands.Up)
                time.sleep(1)

    # Callback must take 1 parameter (bool, indicating if penetrated)
    def penetrate_ring(self, callback, analyzer):
        self.approach_ring(analyzer)
        print 'penetrating'
        passed = False

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
        approached = False
        while not approached:
            # TODO: Implement. Drone should be directly in front of ring/QR code
            qr_center = analyzer.get_qr_center()
            if abs(qr_center[0]) < 20 and abs(qr_center[1]) < 20:
                # Centered
                print 'approached'
                approached = True
            else:
                command = _determine_movement(qr_center)
                self.send_command(command)
            command = None  # TODO
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
    if center[0] > center[1]:
        if center[0] > 0:
            return Commands.Right
        else:
            return Commands.Left
    else:
        if center[1] > 0:
            return Commands.Down
        else:
            return Commands.Up
