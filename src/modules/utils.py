# Credit https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import struct


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
        #print 'QR code: ', qr_txt


def distance_analyzer(rx, ry, cx, cy):
    dx = cx-rx
    dy = cy-ry
    cord = [dx, dy]
    return cord


def float_to_bits(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]


def get_rect_points(polygon):
    tr = br = max(polygon)
    polygon.remove(tr)
    point = max(polygon)
    if point.y > br.y:
        br = point
    else:
        tr = point
    polygon.remove(point)
    tl = bl = polygon[0]
    polygon.remove(tl)
    point = polygon[0]
    if point.y > bl.y:
        bl = point
    else:
        tl = point
    return [tr, br, bl, tl]


def get_rect_padding(tr, br, bl, tl, width, height):
        min_x = min(tl.x, bl.x)
        max_x = max(tr.x, br.x)
        min_y = min(tl.y, tr.y)
        max_y = min(bl.y, br.y)

        padding_top = min_y
        padding_bottom = height - max_y
        padding_left = min_x
        padding_right = width - max_x

        return [padding_top, padding_right, padding_bottom, padding_left]
