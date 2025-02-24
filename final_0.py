import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def grayscale(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def kreiserkennung(image, minR, maxR):
    result = image
    gray = grayscale(image)
    img = cv.medianBlur(gray, 5)

    rows = img.shape[0]

    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=minR, maxRadius=maxR)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(result, center, 1, (255, 0, 255), 3)
            # circle outline
            radius = i[2]
            cv.circle(result, center, radius, (255, 0, 255), 3)
    else:
        return result
    return result


def kantenerkennung(image, minVal=100, maxVal=200):
    image = grayscale(image)
    #cv.imshow('Image', image)
    assert image is not None, "file could not be opened"
    edges = cv.Canny(image, minVal, maxVal)
    # plt.subplot(121), plt.imshow(image, cmap='gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    return edges

def save_image(image, path):
    cv.imwrite(path, image)

def open_image(path):
    img = cv.imread(path, cv.IMREAD_COLOR)
    return img

def increase_brightness(image, value=10):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def decrease_brightness(image, value=30):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    v = cv.subtract(v, value)
    v[v < 0] = 0
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img