import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from src.modules.qranalyzer import decode
from src.modules.qranalyzer import display

if __name__ == '__main__':
    # Read image
    cap = cv2.VideoCapture(0)


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
            # convert the (x, y) coordinates and radius of the circles to iqqntegers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle in the image
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                decodedObjects = decode(frame)
                display(frame, decodedObjects)

        # Display the resulting frame
        cv2.imshow('frame', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture if you quit
    cap.release()
    cv2.destroyAllWindows()
