from interfaces import Commander, Priority
# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]

import cv2
import numpy as np
# Inspired by https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

cap = cv2.VideoCapture("nemt.avi")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    # Finds the cirles in the stream
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=100, minRadius=0, maxRadius=0)

    # If there is cirles, draw then on the feed
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle in the image
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture if you quit
cap.release()
cv2.destroyAllWindows()

class Analyzer(Commander):
    _ring_observers = set()
    _analyzed_video_observers = set()
    _analyzing = False

    def analyze_video(self, video_URL, rings):
        priority = Priority.Analyzing
        video = None  # TODO: cv2.VideoCapture(video_URL)
        # Analyzes the video and searches for rings
        # video is the resulting object of cv2.VideoCapture(video_URL)
        # Rings contains all previously found rings
        # If a new ring is found, call _ring_observer_callback()
        # Always call _analyzed_video_observer_callback()
        ret, frame = video.read()
        while self._analyzing and ret:
            # TODO: Analyze the video
            if False:
                # If specific drone movement is needed for analysis, call send_command()
                command = None  # TODO
                self.send_command(command, priority)
            ring = None  # TODO: Any ring found in the analysis - loop if multiple
            if not rings.contains(ring):
                self._ring_observer_callback(ring)
            analyzed_video = None  # TODO: A single, analyzed/augmented frame
            self._analyzed_video_observer_callback(analyzed_video)
            pass

    def start(self):
        # TODO: Check if analyzer-thread is running, create it if not
        self._analyzing = True

    def pause(self):
        self._analyzing = False

    def stop(self):
        # TODO: Check if analyzer-thread is running, close if it is
        self._analyzing = False

    def _analyzed_video_observer_callback(self, analyzed_video):
        for obs in self._analyzed_video_observers:
            obs.receive_analyzed_video(analyzed_video)

    def _ring_observer_callback(self, ring):
        for obs in self._ring_observers:
            obs.add_ring(ring)

    def add_ring_observer(self, obs):
        self._ring_observers.add(obs)

    def del_ring_observer(self, obs):
        try:
            self._ring_observers.remove(obs)
        except KeyError:
            pass  # TODO

    def add_analyzed_video_observer(self, obs):
        self._analyzed_video_observers.add(obs)

    def del_analyzed_video_observer(self, obs):
        try:
            self._analyzed_video_observers.remove(obs)
        except KeyError:
            pass  # TODO
