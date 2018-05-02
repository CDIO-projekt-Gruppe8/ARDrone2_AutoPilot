# TODO: Sanity and type check in all setter methods
# TODO: Equality method (equal QR numbers?)


class Ring(object):
    position = [0, 0, 0]
    radius = 0
    qr_number = -1
    passed = False

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def get_qr_number(self):
        return self.qr_number

    def set_qr_number(self, qr_number):
        self.qr_number = qr_number

    def get_passed(self):
        return self.passed

    def set_passed(self, passed):
        self.passed = passed
