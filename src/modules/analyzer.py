# TODO: Sanity and type check on all add/delete methods
# TODO: Implement analyze_video()
# TODO: analyze_video() should run in a separate thread [this also affects start() and stop()]

import numpy as np #Install numpy to use the import numpy
import cv2 #Install opencv-python to use the import cv2
from src.modules.qranalyzer import decode
from src.modules.qranalyzer import display
from src.modules.distanceanalyzer import distanceanalyzer

# Inspired by https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

class Analyzer(object):
    _ring_observers = set()
    _analyzing = False

    def analyze_video(self, video_url, current_qr_number):
        # Color definition
        lowerBound1=np.array([170,50,50])
        upperBound1=np.array([180,255,255])

        lowerBound2=np.array([0,50,50])
        upperBound2=np.array([10,255,255])

        qrStatus = 0
        circlesStatus = 0
        # Initiate video capture
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            #  Finds center of frame and draw it on frame
            height, width = frame.shape[:2]
            cv2.rectangle(frame, ((width/2) - 5, (height/2) - 5), ((width/2) + 5, (height/2) + 5), (220, 220, 220), -1)

            # Ring operations on the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            gray = cv2.medianBlur(gray, 5)

            # Color operations on the frame
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color1 = cv2.inRange(hsv, lowerBound1, upperBound1)
            color2 = cv2.inRange(hsv, lowerBound2, upperBound2)
            color = color1+color2

            res = cv2.bitwise_and(frame, frame, mask=color)
            res2 = cv2.bitwise_and(frame, frame, mask=color1)
            res3 = cv2.bitwise_and(frame, frame, mask=color2)

            # Finds the cirles in the frames
            #  Gray
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=40, param2=100, minRadius=0, maxRadius=0)

            #  Red
            #  circles = cv2.HoughCircles(color, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=30, minRadius=0, maxRadius=0)

            # Decodes a QR code
            decodedObjects = decode(frame)

            # If there are QRCODES, draw then on the video feed
            if len(decodedObjects) is not 0:
                display(frame, decodedObjects)
                qrStatus = 1
                qrStatusString = "QR STATUS: QR FOUND"
                for obj in decodedObjects:
                    qrtop = obj.rect[1]
                    qrheight = obj.rect[3]
                    qr = obj.rect, qrtop, qrheight
                    qrData = obj.data
                    print qr

            else:
                qrStatus = 0
                qrStatusString = "QR STATUS: QR NOT FOUND"

            # If there are circles, draw then on the video feed
            if circles is not None:
                circlesStatus = 1
                circlesStatusString = "Circle Status: Circle FOUND"

                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")

                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle in the image
                    # corresponding to the center of the circle
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                    #  calculate the distance form the center of the ring to the center of the frame and show it
                    cv2.line(frame, (x, y), (width/2, height/2), (220, 220, 220), 1)
                    distance = distanceanalyzer(x, y, width/2, height/2)
                    distanceString = map(int, distance)
                    cv2.putText(frame, repr(distanceString), (((x+(width/2))/2), ((y+(height/2))/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (102, 0, 255), 1)

            else:
                circlesStatus = 0
                circlesStatusString = "Circle Status:  Circle NOT FOUND"

            #  Draw box around both objects
            if qrStatus is 1 and circlesStatus is 1:
                cv2.rectangle(frame, (x + r+10, y - r-10), (x - r-10, qrtop + qrheight+10), (0, 128, 255), 1)
                objectString = 'RingObject ' + qrData + ' found'
                cv2.putText(frame, objectString, (x - r-10, y - r-12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 255), 2)
                self._ring_observer_callback()
                self.set_ring_center(distance)
                print distance
                break


            # Display the resulting frame
            cv2.putText(frame, qrStatusString, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(102, 0, 255), 1)
            cv2.putText(frame, circlesStatusString, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(102, 0, 255), 1)
            cv2.imshow('Ring Detection',frame)

            #cv2.imshow('Color',res)
            #  cv2.imshow('Color1', res2)
            #  cv2.imshow('Color2', res3)
            #  print 'qr status: ', qrStatus
            #  print 'circle status', circlesStatus

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the capture if you quit
        cap.release()
        cv2.destroyAllWindows()


        # Analyzes the video and searches for rings
        # video is the resulting object of cv2.VideoCapture(video_URL)
        # Rings contains all previously found rings
        # If a new ring is found, call _ring_observer_callback()
        #while self._analyzing and ret:
            # TODO: Analyze the video
            #qr_number = None
            #if qr_number is current_qr_number:
                # Found the ring of interest. Stop analyzing.
                #self._ring_observer_callback()
                #break
            #pass

    def __init__(self, distance):
        self.distance = distance

    def get_ring_center(self):
        # Returns the x-y coordinates of the ring
        return self.distance

    def set_ring_center(self, distance):
        # Sets the x-y coordinates of the ring
        self.distance = distance

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
