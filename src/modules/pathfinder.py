import time
from interfaces import Commander, Commands
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False

    def explore(self):

        Ross = 0
        while self._exploring:
            qrStatus = 0  # qrStatus ??
            # self.send_command(setspeed.drone(0.3))
            # self.send_command(drone.takeoff)

            if Ross is 4:
                self.send_command(Commands.Up)
                # self.send_command(drone.moveup)
                time.sleep(2)
                Ross = 0

            self.command_send(drone.turnAngle(90))  # 90 grader ??
            Ross = Ross + 1
        while self._exploring:
            # TODO: Define the exploration behaviour of the drone
            # Should it move directly forward until it would hit a wall, then turn sharply?
            # Should it turn slowly while moving in random directions?
            command = None  # TODO
            self.send_command(command)
        pass

    # Callback must take 1 parameter (bool, indicating if penetrated)
    def penetrate_ring(self, qr_number, callback, analyzer):
        self.approach_ring(qr_number, analyzer)
        passed = False
        while not passed:
            # TODO: Implement logic to enter the ring and determine when the ring is passed
            command = None  # TODO
            self.send_command(command)
        # Ring is now passed or loop escaped for some reason
        if callback is not None:
            callback(passed)
        pass

    def approach_ring(self, qr_number, analyzer):
        approached = False
        while not approached:
            # TODO: Implement. Drone should be directly in front of ring/QR code
            center = analyzer.get_ring_center(qr_number)
            command = None  # TODO
            self.send_command(command)
        pass

    def start(self):
        # TODO: Check if pathfinder-thread is running, create it if not
        self._exploring = True

    def pause(self):
        self._exploring = False

    def stop(self):
        # TODO: Check if pathfinder-thread is running, close if it is
        self._exploring = False
