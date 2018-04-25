from src.interfaces import CommandObserver, RingObserver
from src.modules.analyzer import Analyzer
from src.modules.pathfinder import Pathfinder
from src.modules.communication import Communication
# TODO: Implement run(), initiate_drone_configuration(), receive_command(), add_ring()


class Drone(CommandObserver, RingObserver):
    def __init__(self):
        self._number_of_rings = 10
        self._current_ring = 0
        self._rings = [None] * self._number_of_rings
        self._analyzer = Analyzer(self)
        self._communication = Communication()
        self._pathfinder = Pathfinder(self)

    def run(self):
        """
        PSEUDO CODE:

        Test communications
        initiate analyzer
        initiate pathfinder
        START EXPLORE
        """
        pass

    def initiate_drone_configuration(self):
        pass

    def receive_command(self, command, priority):
        # TODO: Command is received from analyzer of pathfinder, determine how to react based on priority
        pass

    def add_ring(self, ring):
        # TODO: Ring is found by analyzer (probably while exploring), add it to the list of rings
        """
        PSEUDO CODE:

        rings[ring.qr] = ring
        if ring.qr == _current_ring:
            PAUSE EXPLORE
            PENETRATE

            when PENETRATE is done:
                if ring.qr == _number_of_rings:
                    STOP EXPLORE
                    STOP ANALYZER
                    LAND DRONE
                else:
                    START EXPLORE
        """
        pass
