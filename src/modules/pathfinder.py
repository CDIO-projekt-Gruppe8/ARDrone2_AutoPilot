import time
from src.interfaces import Commander, Commands
# TODO: Sanity check on rings
# TODO: Implement explore(), penetrate_ring(), approach_ring()
# TODO: (while loops of) explore(), penetrate_ring(), approach_ring() should all run in a separate thread


class Pathfinder(Commander):
    _exploring = False
    _frame_width = 640
    _frame_height = 480

    def explore(self):
        while True:
            if self._exploring:
                print 'exploring'
                for i in range(0, 4):
                    self.send_command(Commands.RotateRight)
                    time.sleep(0.5)
                    self.send_command(Commands.Hover)
                    time.sleep(1)
                    if not self._exploring:
                        break
                if not self._exploring:
                    continue
                self.send_command(Commands.Up)
                time.sleep(0.5)

    # Callback must take 1 parameter (bool, indicating if penetrated)
    def penetrate_ring(self, callback, analyzer):
        approached = self.approach_ring(analyzer)
        if not approached:
            print 'could not approach'
            if callback is not None:
                callback(False)
            return
        print 'penetrating'
        self.send_command(Commands.Up)
        time.sleep(0.2)
        self.send_command(Commands.Hover)
        time.sleep(0.5)
        # Move forward
        self.send_command(Commands.Forward)
        time.sleep(1.0)
        self.send_command(Commands.Hover)
        # Ring is now passed or loop escaped for some reason
        print 'Penetration done'
        if callback is not None:
            callback(True)

    def approach_ring(self, analyzer):
        self.send_command(Commands.Hover)
        time.sleep(1)
        self.adjust_angle(analyzer)
        print 'approaching'
        no_qr_timer = None
        while True:
            qr_polygon, qr_center, qr_padding = analyzer.get_qr()
            if qr_center is None:
                if no_qr_timer is None:
                    print 'Unable to see QR'
                    no_qr_timer = time.clock()
                elif time.clock() - no_qr_timer > 5:
                    return False
                continue
            no_qr_timer = None
            if max(qr_padding) < 120:
                print 'approached'
                return True
            command = _determine_movement(qr_padding)
            self.send_command(command)
            time.sleep(0.5)
            self.send_command(Commands.Hover)

    def adjust_angle(self, analyzer):
        print 'adjusting angle'
        while True:
            qr_polygon, _, _ = analyzer.get_qr()
            if qr_polygon[0] is None:
                time.sleep(0.1)
                continue
            right_height = qr_polygon[1].y - qr_polygon[0].y
            left_height = qr_polygon[2].y - qr_polygon[3].y
            init_ratio = float(left_height)/float(right_height)
            if abs(1 - init_ratio) < 0.01:
                print 'angle has been adjusted'
                time.sleep(1)
                break
            else:
                print 'L: ' + str(left_height) + ' / R: ' + str(right_height) \
                      + ' = ' + str(init_ratio)

            # Check if QR Code is about to leave image from top / bottom
            if left_height > right_height:
                if self._frame_width - max(qr_polygon[0].x, qr_polygon[1].x) < 100:
                    direction = Commands.Right
                else:
                    direction = Commands.RotateLeft
            else:
                if min(qr_polygon[2].x, qr_polygon[3].x) < 100:
                    direction = Commands.Left
                else:
                    direction = Commands.RotateRight
            self.send_command(direction)
            time.sleep(0.5)
            self.send_command(Commands.Hover)
            time.sleep(1)

    def start(self):
        # TODO: Check if pathfinder-thread is running, create it if not
        self._exploring = True

    def pause(self):
        self._exploring = False

    def stop(self):
        # TODO: Check if pathfinder-thread is running, close if it is
        self._exploring = False


# Static functions
def _get_qr_polygon(analyzer):
    return analyzer.get_qr_polygon()


def _determine_movement(qr_padding):
    [padding_top, padding_right, padding_bottom, padding_left] = qr_padding
    padding_diff_vertical = padding_top - padding_bottom
    padding_diff_horizontal = padding_right - padding_left

    if abs(padding_diff_vertical - padding_diff_horizontal) < 20:
        return Commands.Forward
    elif abs(padding_diff_vertical) > abs(padding_diff_horizontal):
        if padding_diff_vertical > 0:
            return Commands.Down
        else:
            return Commands.Up
    else:
        if padding_diff_horizontal > 0:
            return Commands.Left
        else:
            return Commands.Right
