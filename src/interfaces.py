class Commander(object):
    def __init__(self):
        self._command_observers = set()

    def send_command(self, command, priority):
        # priority should be a Priority object
        for obs in self._command_observers:
            obs.receive_command(command, priority)

    def add_command_observer(self, obs):
        self._command_observers.add(obs)

    def del_command_observer(self, obs):
        self._command_observers.remove(obs)


class CommandObserver(object):
    def receive_command(self, command, priority):
        pass


class RingObserver(object):
    def add_ring(self, ring):
        pass


class AnalyzedCamObserver(object):
    def receive_analyzed_video(self, stream):
        pass


class Priority(object):
    Exploring, Approaching, Analyzing, Penetrating = range(4)
