import time
from interfaces import CommandObserver, RingObserver
from modules.analyzer import Analyzer
from modules.pathfinder import Pathfinder
from modules.communication import Communication
# TODO: Implement run(), initiate_drone_configuration(), receive_command(), add_ring()


class Drone(CommandObserver, RingObserver):

    _penetrating = False

    def __init__(self):
        print("Drone initiating")
        self._analyzer = Analyzer()
        self._communication = Communication()
        self._pathfinder = Pathfinder()

        self._video_url = "tcp://localhost:5555"  # TODO: Insert correct URL
        self._number_of_rings = 10  # TODO: Real number? Determine dynamically? How long should it search?
        self._current_ring = 0
        self._rings = [None] * self._number_of_rings
        self._command = None

    def run(self):
        ready, msg = self._communication.test()
        if ready:
            print("Take off with msg: " + msg)
            # Listen for events
            self.add_command_observer(self)
            self.add_ring_observer(self)
            # Initiate analyzer
            self._analyzer.start()
            self._analyzer.analyze_video(self._video_url, self._rings)
            # Initiate pathfinder
            self._pathfinder.explore()
            self._pathfinder.start()
        else:
            print(msg)

    def _initiate_drone_configuration(self):
        # TODO: Implement
        pass

    def receive_command(self, command):
        self._command = command

    def _send_command(self):
        while True:
            time.sleep(0.03)
            if self._command is not None:
                self._communication.move(self._command)
                self._command = None  # TODO: Variable should be locked
        pass

    def add_ring(self, ring):
        self._rings[ring.get_qr_number()] = ring
        if ring.get_qr_number() is self._current_ring:
            self._pathfinder.pause()
            self._pathfinder.penetrate_ring(ring, self._update_state())

    def _update_state(self):
        if self._current_ring == self._number_of_rings:
            # Final ring penetrated - exit the game
            self._pathfinder.stop()
            self._analyzer.stop()
            self._communication.land()
        else:
            # More rings to penetrate - continue exploring
            self._pathfinder.start()

    def add_command_observer(self, observer):
        self._pathfinder.add_command_observer(observer)
        self._analyzer.add_command_observer(observer)

    def add_ring_observer(self, observer):
        self._analyzer.add_ring_observer(observer)

    def add_analyzed_video_observer(self, observer):
        self._analyzer.add_analyzed_video_observer(observer)

    def del_command_observer(self, observer):
        self._pathfinder.del_command_observer(observer)
        self._analyzer.del_command_observer(observer)

    def del_ring_observer(self, observer):
        self._analyzer.del_ring_observer(observer)

    def del_analyzed_video_observer(self, observer):
        self._analyzer.del_analyzed_video_observer(observer)
