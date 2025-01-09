import cv2
import numpy as np
import matplotlib.pyplot as plt

def grayscale(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img

def hough_lines(img):

    #Get image dimension

    Nx = img.shape[0]
    Ny = img.shape[1]

    Maxdist = int(np.round(np.sqrt(Nx**2 + Ny ** 2)))

    thetas = np.deg2rad(np.arange(-90, 90))

    rs = np.linspace(-Maxdist, Maxdist, 2*Maxdist)

    accumulator = np.zeros((2 * Maxdist, len(thetas)))

    for x in range(Ny):
        for y in range(Nx):
            # Check if it is an edge pixel
            #  NB: y -> rows , x -> columns
            if img[y, x] > 0:
                for k in range(len(thetas)):
                    r = x * np.cos(thetas[k]) + y * np.sin(thetas[k])
                    accumulator[int(r) + Maxdist, k] += 1

    return accumulator, thetas, rs

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


def draw_detected_lines(img, accumulator, thetas, rhos, threshold=50):
    lines = []
    for r_idx in range(accumulator.shape[0]):
        for t_idx in range(accumulator.shape[1]):
            if accumulator[r_idx, t_idx] > threshold:
                rho = rhos[r_idx]
                theta = thetas[t_idx]
                lines.append((rho, theta))

    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return img

#idx = np.argmax(accumulator)
#rho = int(rhos[int(idx / accumulator.shape[1])])
#theta = thetas[int(idx % accumulator.shape[1])]
#print("rho={0:.0f}, theta={1:.0f}".format(rho, np.rad2deg(theta)))

# # Main code line
# path = 'building.jpg'
# src = cv2.imread(path)
# image = grayscale(path)
#
# edges = cv2.Canny(image, 100, 200)
#
# accumulator, thetas, rhos = hough_lines(edges)
#
# # Draw lines on a copy of the original image
# output_image = src.copy()
# output_image_with_lines = draw_detected_lines(output_image, accumulator, thetas, rhos, threshold=100)

# Plot results
# plt.figure('Original Image')
# plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
# plt.figure('Edges')
# plt.imshow(edges, cmap='gray')
# plt.figure('Hough Space')
# plt.imshow(accumulator, cmap='gray')
# plt.figure('Detected Lines')
# plt.imshow(cv2.cvtColor(output_image_with_lines, cv2.COLOR_BGR2RGB))
# plt.show()

# Main code circle
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

plt.figure('Original Image')
plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
plt.figure('Detected Circles')
plt.imshow(cv2.cvtColor(output_image_with_circles, cv2.COLOR_BGR2RGB))
plt.show()