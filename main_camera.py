import cv2

import utils
import cv_maze

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while utils.wait_frame():
    ret, frame = camera.read()

    if not ret:
        break

    utils.display_image("Camera", frame)

    try:
        path = cv_maze.solve_maze(frame)
    except Exception as e:
        print(e)
        continue

    # draw the path on the original image
    for i in range(len(path) - 1):
        cv2.line(frame, path[i], path[i + 1], (0, 255, 0), 5)

    utils.display_image("Solution", frame)

camera.release()
