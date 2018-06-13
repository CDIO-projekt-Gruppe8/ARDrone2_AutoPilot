class Commander(object):
    def __init__(self):
        self._command_observers = set()

    def send_command(self, command):
        # priority should be a Priority object
        for obs in self._command_observers:
            obs.receive_command(command)

    def add_command_observer(self, obs):
        self._command_observers.add(obs)

    def del_command_observer(self, obs):
        self._command_observers.remove(obs)


class CommandObserver(object):
    def receive_command(self, command):
        pass


class RingObserver(object):
    def ring_found(self):
        pass


class Commands(object):
    Up, Down, Left, Right, Forward, Back, RotateLeft, RotateRight = range(8)

