# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]

import time
import cv2  # Install opencv-python to use the import cv2
from utils import decode_qr
from utils import display_qr
from utils import distance_analyzer
from utils import get_rect_points, get_rect_padding

# Inspired by https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/


class Analyzer(object):
    _ring_observers = set()
    _analyzing = False
    _qr_center = None
    _qr_polygon = None
    _qr_padding = [None] * 4
    _current_qr_number = None
    _command = None

    def analyze_video(self, video_url, current_qr_number):
        # TODO: REM
        video_url = 1
        # TODO: DONE
        self.set_current_qr(current_qr_number)
        print 'analyze beginning'
        # Initiate video capture
        cap = cv2.VideoCapture(video_url)
        # Capture first frame
        ret, frame = cap.read()

        # Get current width of frame
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # Get current height of frame
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        FILE_OUTPUT = 'C:\Users\ymuslu\Desktop\output_' \
                      + time.strftime("%y%d%m_%H%M%S", time.gmtime()) + '.avi'
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter.fourcc(*'XVID')
        out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 20.0, (width, height))

        print 'while loop beginning'
        while self._current_qr_number is not None:
            if not ret:
                cap = cv2.VideoCapture(video_url)
                ret, frame = cap.read()
                if not ret:
                    time.sleep(1)
                    continue
            out.write(frame)
            #  Finds center of frame and draw it on frame
            cv2.rectangle(frame, ((width/2) - 5, (height/2) - 5), ((width/2) + 5, (height/2) + 5), (102, 0, 255), -1)

            # Decodes a QR code
            decoded_objects = decode_qr(frame)

            # If there are QR , draw then on the video feed
            qr_status_string = "QR STATUS: QR NOT FOUND"
            qr_status = False
            qr_polygon = None
            if len(decoded_objects) is not 0:
                display_qr(frame, decoded_objects)
                qr_status_string = "QR STATUS: QR FOUND"
                for obj in decoded_objects:
                    qr_data = obj.data
                    qr_status_string = "QR STATUS: QR FOUND [" + qr_data + "]"
                    if qr_data == self._current_qr_number:
                        [qr_tr, qr_br, qr_bl, qr_tl] = get_rect_points(obj.polygon)
                        self.set_qr_padding(qr_tr, qr_br, qr_bl, qr_tl, width, height)
                        qr_left = obj.rect[0]
                        qr_top = obj.rect[1]
                        qr_width = obj.rect[2]
                        qr_height = obj.rect[3]

                        qr_x = qr_left + (qr_width/2)
                        qr_y = qr_top + (qr_height/2)

                        qr_polygon = [qr_tr, qr_br, qr_bl, qr_tl]
                        qr_center = distance_analyzer(qr_x, qr_y, width / 2, height / 2)
                        qr_status = True
                        cv2.line(frame, (qr_x, qr_y), (width/2, height/2), (102, 0, 255), 1)
                        cv2.circle(frame, qr_tl, 5, (102, 0, 255), 2)
                        cv2.circle(frame, qr_tr, 5, (102, 0, 255), 2)
                        cv2.circle(frame, qr_bl, 5, (102, 0, 255), 2)
                        cv2.circle(frame, qr_br, 5, (102, 0, 255), 2)
                        cv2.putText(frame, 'TL: [' + str(qr_tl.x) + ', ' + str(qr_tl.y) + ']',
                                    (qr_tl.x, qr_tl.y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 2)
                        cv2.putText(frame, 'BL: [' + str(qr_bl.x) + ', ' + str(qr_bl.y) + ']',
                                    (qr_bl.x, qr_bl.y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 2)
                        cv2.putText(frame, 'TR: [' + str(qr_tr.x) + ', ' + str(qr_tr.y) + ']',
                                    (qr_tr.x + 20, qr_tr.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 2)
                        cv2.putText(frame, 'BR: [' + str(qr_br.x) + ', ' + str(qr_br.y) + ']',
                                    (qr_br.x + 20, qr_br.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 2)
                        break
            if not qr_status:
                qr_polygon = [None] * 4
                qr_center = None
            self.set_qr_polygon(qr_polygon, qr_center, width, height)

            #  Draw box around both objects and sets coordinates of ring center
            if qr_status and self._analyzing:
                self._analyzing = False
                self._ring_observer_callback()

            # Display the resulting frame
            cv2.putText(frame, qr_status_string, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 1)
            cv2.putText(frame, self._command, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 1)
            cv2.imshow('Ring Detection', frame)
            cv2.waitKey(1)
            if 0xFF == ord('q'):
                break

            # Capture frame-by-frame
            ret, frame = cap.read()

        # Release the capture if you quit
        print 'while loop exited'
        out.release()
        cap.release()
        cv2.destroyAllWindows()

    def set_command(self, command):
        self._command = command

    def set_current_qr(self, qr):
        self._current_qr_number = qr

    def set_qr_polygon(self, qr_polygon, qr_center, width, height):
        self._qr_polygon = None
        [tr, br, bl, tl] = qr_polygon
        if tr is None or br is None or bl is None or tl is None:
            self._qr_padding = [None] * 4
        else:
            self.set_qr_padding(tr, br, bl, tl, width, height)
        self.set_qr_center(qr_center)
        self._qr_polygon = qr_polygon

    def set_qr_center(self, qr_center):
        self._qr_center = qr_center

    def set_qr_padding(self, tr, br, bl, tl, width, height):
        self._qr_padding = get_rect_padding(tr, br, bl, tl, width, height)

    def get_qr(self):
        if self._qr_polygon is None:
            return None, None, None
        return self._qr_polygon, self._qr_center, self._qr_padding

    def start(self):
        # Check if analyzer-thread is running, create it if not
        if self._analyzing is not True:
            self._analyzing = True

    def pause(self):
        self._analyzing = False

    def stop(self):
        # Check if analyzer-thread is running, close if it is
        if self._analyzing is True:
            self._analyzing = False
        self.set_current_qr(None)

    def _ring_observer_callback(self):
        for obs in self._ring_observers:
            obs.ring_found()

    def add_ring_observer(self, obs):
        self._ring_observers.add(obs)

    def del_ring_observer(self, obs):
        try:
            self._ring_observers.remove(obs)
        except KeyError:
            print "Error at deleting ring observer"
            # pass TODO
