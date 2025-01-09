import cv2
import numpy as np
import matplotlib.pyplot as plt

def grayscale(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img

def hough_circles(img, min_radius, max_radius, threshold):
    Ny, Nx = img.shape  # Nx = width, Ny = height
    radius_range = max_radius - min_radius
    accumulator = np.zeros((Ny, Nx, radius_range), dtype=np.uint64)

    edges = cv2.Canny(img, 100, 200)

    edge_points = np.argwhere(edges > 0)
    for y, x in edge_points:
        for r in range(min_radius, max_radius):
            for theta in np.arange(0, 360, 1):
                theta_rad = np.deg2rad(theta)
                x0 = int(x - r * np.cos(theta_rad))
                y0 = int(y - r * np.sin(theta_rad))
                if 0 <= x0 < Nx and 0 <= y0 < Ny:
                    accumulator[y0, x0, r - min_radius] += 1

    detected_circles = []
    for r in range(radius_range):
        for x0 in range(Nx):
            for y0 in range(Ny):
                if accumulator[y0, x0, r] > threshold:
                    detected_circles.append((x0, y0, r + min_radius))

    return detected_circles

def draw_detected_circles(img, circles):
    for x0, y0, r in circles:
        cv2.circle(img, (x0, y0), r, (0, 255, 0), 2)
        cv2.circle(img, (x0, y0), 2, (0, 0, 255), 3)
    return img

# Main code
path = 'smarties.png'
src = cv2.imread(path)
image = grayscale(path)

# Hough Circle Detection
min_radius = 1
max_radius = 60
threshold = 150

detected_circles = hough_circles(image, min_radius, max_radius, threshold)

# Draw circles on the original image
output_image = src.copy()
output_image_with_circles = draw_detected_circles(output_image, detected_circles)

# Plot results
# plt.figure('Original Image')
# plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
# plt.figure('Detected Circles')
# plt.imshow(cv2.cvtColor(output_image_with_circles, cv2.COLOR_BGR2RGB))
# plt.show()