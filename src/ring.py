# TODO: Sanity and type check in all setter methods
# TODO: Equality method (equal QR numbers?)


class Ring(object):
    _position = [0, 0, 0]
    _radius = 0
    _qr_number = -1
    _passed = False

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def get_radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius

    def get_qr_number(self):
        return self._qr_number

    def set_qr_number(self, qr_number):
        self._qr_number = qr_number

    def get_passed(self):
        return self._passed

    def set_passed(self, passed):
        self._passed = passed
