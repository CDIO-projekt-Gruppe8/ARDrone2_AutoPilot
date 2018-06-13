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

        self._video_url = "tcp://192.168.1.1:5555"  # TODO: Insert correct URL
        self._number_of_rings = 10  # TODO: Real number? Determine dynamically? How long should it search?
        self._current_qr_number = 1
        self._command = None

    def run(self):
        ready, msg = self._communication.test()
        if ready:
            self._communication.set_max_altitude()
            print("Take off with msg: " + msg)
            # Listen for events
            self.add_command_observer(self)
            self.add_ring_observer(self)
            # Initiate pathfinder
            self._pathfinder.explore()
            self._pathfinder.start()
            # Initiate analyzer
            self._analyzer.start()
            self._analyzer.analyze_video(self._video_url, self._current_qr_number)
        else:
            print(msg)

    def receive_command(self, command):
        self._command = command

    def _send_command(self):
        while True:
            time.sleep(0.03)  # ARDrone claims to work best with commands every 0.03 sec
            if self._command is not None:
                self._communication.move(self._command)
        pass

    def _shutdown(self):
        self._pathfinder.stop()
        self._analyzer.stop()
        self._communication.land()

    def ring_found(self):
        self._penetrate()

    def _ring_passed(self, passed):
        if not passed:
            print('Failed at passing ring!')
            print('Trying again')
            self._penetrate()
        else:
            if self._current_qr_number == self._number_of_rings:
                self._shutdown()
            else:
                self._penetrating = False
                self._current_qr_number += 1
                self._pathfinder.start()
                self._analyzer.analyze_video(self._video_url, self._current_qr_number)

    def _penetrate(self):
        self._penetrating = True
        self._pathfinder.pause()
        self._pathfinder.penetrate_ring(callback=self._ring_passed, analyzer=self._analyzer)

    def add_command_observer(self, observer):
        self._pathfinder.add_command_observer(observer)

    def add_ring_observer(self, observer):
        self._analyzer.add_ring_observer(observer)

    def del_command_observer(self, observer):
        self._pathfinder.del_command_observer(observer)

    def del_ring_observer(self, observer):
        self._analyzer.del_ring_observer(observer)
