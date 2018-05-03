import time
from interfaces import CommandObserver, RingObserver, Priority
from modules.analyzer import Analyzer
from modules.pathfinder import Pathfinder
from modules.communication import Communication
# TODO: Implement run(), initiate_drone_configuration(), receive_command(), add_ring()


class Drone(CommandObserver, RingObserver):

    _penetrating = False

    def __init__(self):
        self._analyzer = Analyzer()
        self._communication = Communication()
        self._pathfinder = Pathfinder()

        self._video_URL = "tcp://localhost:5555"
        self._number_of_rings = 10  # TODO: Real number? Determine dynamically? How long should it search?
        self._current_ring = 0
        self._rings = [None] * self._number_of_rings
        self._commands = {Priority.Exploring: None, Priority.Approaching: None, Priority.Analyzing: None,
                          Priority.Penetrating: None}

    def run(self):
        ready, msg = self._communication.test()
        if ready:
            # Initiate analyzer
            self._analyzer.add_command_observer(self)
            self._analyzer.add_command_observer(self)
            self._analyzer.analyze_video(self._video_URL, self._rings)
            self._analyzer.start()
            # Initiate pathfinder
            self._pathfinder.add_command_observer(self)
            self._pathfinder.explore()
            self._pathfinder.start()
        else:
            print(msg)

    def _initiate_drone_configuration(self):
        # TODO: Implement
        pass

    def receive_command(self, command, priority):
        self._commands[priority] = command

    def _send_command(self):
        while True:
            time.sleep(0.03)
            if self._penetrating and self._commands[Priority.Penetrating] is None:
                continue
            else:
                command = next((el for el in self._commands if el is not None), None)
            if command is not None:
                self._communication.move(command)
        pass

    def add_ring(self, ring):
        self._rings[ring.get_qr_number()] = ring
        if ring.get_qr_number() is self._current_ring:
            self._pathfinder.pause()
            self._pathfinder.penetrate_ring(ring, self.update_state())

    def update_state(self):
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
