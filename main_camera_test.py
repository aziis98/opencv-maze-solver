import cv2

import numpy as np
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

    # convert the image to grayscale
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # extract the tags
    tag_registry = utils.extract_tags_dict_single(image_gray)

    # draw borders around the tags
    for r in tag_registry.values():
        (ptA, ptB, ptC, ptD) = r.corners

        cv2.line(frame, np.int32(ptA), np.int32(ptB), (0, 255, 0), 5)
        cv2.line(frame, np.int32(ptB), np.int32(ptC), (0, 255, 0), 5)
        cv2.line(frame, np.int32(ptC), np.int32(ptD), (0, 255, 0), 5)
        cv2.line(frame, np.int32(ptD), np.int32(ptA), (0, 255, 0), 5)

    utils.display_image("Tags", frame)


camera.release()
