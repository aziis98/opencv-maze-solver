import cv2

import utils
import cv_maze

import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image containing AprilTag")
ap.add_argument("-d", "--debug", action="store_true", help="display debug information")
args = vars(ap.parse_args())

# load the input image and convert it to grayscale
print("[INFO] loading image...")

image = cv2.imread(args["image"])
utils.display_image("Image", image)

path = cv_maze.solve_maze(image, debug=args["debug"])

# draw the path on the original image

for i in range(len(path) - 1):
    cv2.line(image, path[i], path[i + 1], (0, 255, 0), 5)

utils.display_image("Solution", image)

utils.wait_close_app()
