from src.interfaces import Commander, Priority
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False

    def explore(self):
        priority = Priority.Exploring
        while self._exploring:
            # TODO: Define the exploration behaviour of the drone
            # Should it move directly forward until it would hit a wall, then turn sharply?
            # Should it turn slowly while moving in random directions?
            command = None  # TODO
            self.send_command(command, priority)
        pass

    def penetrate_ring(self, ring, callback):  # Callback must take 1 parameter (bool, indicating if penetrated)
        priority = Priority.Penetrating
        self.approach_ring(ring)
        passed = False
        while not passed:
            # TODO: Implement logic to enter the ring and determine when the ring is passed
            command = None  # TODO
            self.send_command(command, priority)
        # Ring is now passed or loop escaped for some reason
        if callback is not None:
            callback(passed)
        pass

    def approach_ring(self, ring):
        priority = Priority.Approaching
        approached = False
        while not approached:
            # TODO: Implement. Drone should be directly in front of ring/QR code
            command = None  # TODO
            self.send_command(command, priority)
        pass

    def start(self):
        # TODO: Check if pathfinder-thread is running, create it if not
        self._exploring = True

    def pause(self):
        self._exploring = False

    def stop(self):
        # TODO: Check if pathfinder-thread is running, close if it is
        self._exploring = False
