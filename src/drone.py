import thread
import time
from interfaces import CommandObserver, RingObserver, Commands
from modules.analyzer import Analyzer
from modules.pathfinder import Pathfinder
from modules.communication import Communication
# TODO: Implement run(), initiate_drone_configuration(), receive_command(), add_ring()


class Drone(CommandObserver, RingObserver):

    _finished = False
    _penetrating = False
    _send_commands = True

    def __init__(self):
        print("Drone initiating")
        self._analyzer = Analyzer()
        self._communication = Communication()
        self._pathfinder = Pathfinder()

        self._video_url = "tcp://192.168.1.1:5555"  # TODO: Insert correct URL
        self._number_of_rings = 10  # TODO: Real number? Determine dynamically? How long should it search?
        self._current_qr_number = 7
        self._command = None

    def run(self):
        ready, msg = self._communication.test()
        if ready:
            if self._send_commands:
                self._communication.lift()
                self._communication.set_max_altitude()
            print("Take off with msg: " + msg)
            # Listen for events
            print 'Adding self as observer'
            self.add_command_observer(self)
            self.add_ring_observer(self)
            # Initiate pathfinder
            print 'Initiating pathfinder'
            self._explore()
            # Initiate analyzer
            print 'Initiating analyzer'
            self._analyzer.start()
            self._analyze()
            self._send_command()
        else:
            print(msg)

    def receive_command(self, command):
        self._command = command

    def _send_command(self):
        while not self._finished:
            time.sleep(0.03)  # ARDrone claims to work best with commands every 0.03 sec
            if self._command is not None and self._send_commands:
                self._communication.move(self._command)
                self._command = Commands.Hover
        pass

    def _shutdown(self):
        self._finished = True
        self._pathfinder.stop()
        self._analyzer.stop()
        self._communication.land()

    def ring_found(self):
        self._analyzer.stop()
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
                self._analyzer.start()

    def _analyze(self):
        thread.start_new_thread(self._analyzer.analyze_video, (self._video_url, "P.0" + str(self._current_qr_number)))

    def _explore(self):
        self._pathfinder.start()
        thread.start_new_thread(self._pathfinder.explore, ())
        #self._pathfinder.explore()

    def _penetrate(self):
        self._penetrating = True
        self._pathfinder.pause()
        #self._pathfinder.penetrate_ring(self._ring_passed, self._analyzer)
        thread.start_new_thread(self._pathfinder.penetrate_ring, (self._ring_passed, self._analyzer))

    def add_command_observer(self, observer):
        self._pathfinder.add_command_observer(observer)

    def add_ring_observer(self, observer):
        self._analyzer.add_ring_observer(observer)

    def del_command_observer(self, observer):
        self._pathfinder.del_command_observer(observer)

    def del_ring_observer(self, observer):
        self._analyzer.del_ring_observer(observer)
