# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]

import time
import cv2  # Install opencv-python to use the import cv2
from utils import decode_qr
from utils import display_qr
from utils import distance_analyzer

# Inspired by https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/


class Analyzer(object):
    _ring_observers = set()
    _analyzing = False
    _ring_center = None
    _qr_center = None

    def analyze_video(self, video_url, current_qr_number):
        print 'analyze beginning'
        # Initiate video capture
        cap = cv2.VideoCapture(video_url)
        # Capture first frame
        ret, frame = cap.read()

        print 'while loop beginning'
        while True:
            if not ret:
                cap = cv2.VideoCapture(video_url)
                ret, frame = cap.read()
                if not ret:
                    time.sleep(1)
                    continue
            qr_data = 0
            qr_status = False

        #  Finds center of frame and draw it on frame
            height, width = frame.shape[:2]
            cv2.rectangle(frame, ((width/2) - 5, (height/2) - 5), ((width/2) + 5, (height/2) + 5), (220, 220, 220), -1)

            # Decodes a QR code
            decoded_objects = decode_qr(frame)

            # If there are QR , draw then on the video feed
            qr_status_string = "QR STATUS: QR NOT FOUND"
            if len(decoded_objects) is not 0:
                display_qr(frame, decoded_objects)
                qr_status = True
                qr_status_string = "QR STATUS: QR FOUND"
                for obj in decoded_objects:
                    qr_left = obj.rect[0]
                    qr_top = obj.rect[1]
                    qr_width = obj.rect[2]
                    qr_height = obj.rect[3]
                    qr_data = obj.data
                    if qr_data == current_qr_number:
                        qr_x = qr_left + (qr_width/2)
                        qr_y = qr_top + (qr_height/2)
                        cv2.line(frame, (qr_x, qr_y), (width/2, height/2), (220, 220, 220), 1)
                        self.set_qr_center(
                            distance_analyzer(qr_x, qr_y, width / 2, height / 2))
                        break

            #  Draw box around both objects and sets coordinates of ring center
            if qr_status and qr_data is not None and qr_data == current_qr_number and self._analyzing:
                self._analyzing = False
                self._ring_observer_callback()

            # Display the resulting frame
            cv2.putText(frame, qr_status_string, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 1)
            cv2.imshow('Ring Detection', frame)
            cv2.waitKey(1)
            if 0xFF == ord('q'):
                break

            # Capture frame-by-frame
            ret, frame = cap.read()

        # Release the capture if you quit
        print 'while loop exited'
        cap.release()
        cv2.destroyAllWindows()

    def get_qr_center(self):
        return self._qr_center

    def set_qr_center(self, qr_center):
        self._qr_center = qr_center

    def get_ring_center(self):
        # Returns the x-y coordinates of the ring
        return self._ring_center

    def set_ring_center(self, ring_center):
        # Sets the x-y coordinates of the ring
        self._ring_center = ring_center

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
