import time
import collections
from interfaces import CommandObserver, RingObserver, Priority
from modules.analyzer import Analyzer
from modules.pathfinder import Pathfinder
from modules.communication import Communication
# TODO: Implement run(), initiate_drone_configuration(), receive_command(), add_ring()


class Drone(CommandObserver, RingObserver):

    _penetrating = False

    def __init__(self):
        print("Drone initiating")
        self._analyzer = Analyzer(Priority.Analyzer)
        self._communication = Communication()
        self._pathfinder = Pathfinder(Priority.Pathfinder)

        self._video_url = "tcp://localhost:5555"  # TODO: Insert correct URL
        self._number_of_rings = 10  # TODO: Real number? Determine dynamically? How long should it search?
        self._current_ring = 0
        self._rings = [None] * self._number_of_rings
        self._commands = collections.OrderedDict([
            (Priority.Analyzer, None),
            (Priority.Analyzer, None),
            (Priority.Misc, None)])

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

    def receive_command(self, command, priority):
        self._commands[priority] = command

    def _send_command(self):
        while True:
            time.sleep(0.03)  # ARDrone claims to work best with commands every 0.03 sec
            if self._penetrating:
                command = self._commands[Priority.Pathfinder]
                if command is None:
                    continue  # TODO: Should this be a "hover" command?
            else:
                commander = next((el for el in self._commands if self._commands[el] is not None), None)
                command = self._commands[commander]
                self._commands[commander] = None  # TODO: Should be locked
            if command is not None:
                self._communication.move(command)
        pass

    def _shutdown(self):
        self._pathfinder.stop()
        self._analyzer.stop()
        self._communication.land()

    def add_ring(self, ring):
        self._rings[ring.get_qr_number()] = ring
        self._update_state()

    def _ring_passed(self):
        if self._current_ring == self._number_of_rings:
            self._shutdown()
        else:
            self._current_ring += 1
            self._penetrating = False
            self._update_state()

    def _penetrate(self, ring):
        self._penetrating = True
        self._pathfinder.pause()
        self._pathfinder.penetrate_ring(ring, self._ring_passed())

    def _explore(self):
        self._pathfinder.start()

    # Used as a callback function when calling pathfinder.penetrate_ring()
    # Will be called once the ring has been passed
    def _update_state(self):
        if self._penetrating:
            pass
        else:
            ring = self._rings[self._current_ring]
            if ring is not None:
                # Next ring to penetrate has been found already. Penetrate it
                self._penetrate(ring)
            else:
                # More rings to penetrate - continue exploring
                self._explore()

    def add_command_observer(self, observer):
        self._pathfinder.add_command_observer(observer)

    def add_ring_observer(self, observer):
        self._analyzer.add_ring_observer(observer)

    def add_analyzed_video_observer(self, observer):
        self._analyzer.add_analyzed_video_observer(observer)

    def del_command_observer(self, observer):
        self._pathfinder.del_command_observer(observer)

    def del_ring_observer(self, observer):
        self._analyzer.del_ring_observer(observer)

    def del_analyzed_video_observer(self, observer):
        self._analyzer.del_analyzed_video_observer(observer)
