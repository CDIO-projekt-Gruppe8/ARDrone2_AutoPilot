# Credit https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2


def decode_qr(im):
    return pyzbar.decode(im)


# Display barcode and QR code location
def display_qr(im, decoded_objects):
    # Loop over all decoded objects
    for decoded_object in decoded_objects:
        points = decoded_object.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convex hull
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    for obj in decoded_objects:
        qr_txt = obj.data
        print 'QR code: ', qr_txt


def distance_analyzer(rx, ry, cx, cy):
    dx = cx-rx
    dy = cy-ry
    cord = [dx, dy]
    return cord
