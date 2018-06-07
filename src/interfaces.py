class Commander(object):
    def __init__(self, priority):
        self._priority = priority
        self._command_observers = set()

    def send_command(self, command):
        # priority should be a Priority object
        for obs in self._command_observers:
            obs.receive_command(command, self._priority)

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


class Priority(object):
    Analyzer, Pathfinder, Misc = range(3)
