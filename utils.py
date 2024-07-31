import cv2

import time

import numpy as np

import dt_apriltags
from dt_apriltags import Detector, Detection


WINDOW_LABELS = set()


def display_image(label, image, default_width: int = 800, default_height: int = 600, interpolation: int = cv2.INTER_LINEAR):
    """
    Display an image fitted in a window with the given label and size, optionally setting the interpolation method
    """

    height, width = image.shape[0], image.shape[1]

    if width < default_width or height < default_height:
        new_width = default_height * width // height
        image = cv2.resize(image, (new_width, default_height), interpolation=interpolation)

    WINDOW_LABELS.add(label)
    cv2.namedWindow(label, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(label, default_width, default_height)
    cv2.imshow(label, image)
    cv2.imwrite(f"debug-steps/{len(WINDOW_LABELS):03}_{label}.png", image)


def wait_frame():
    """
    Wait for the user to press any key
    """

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows()
        return False

    if any(cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1 for window in WINDOW_LABELS):
        cv2.destroyAllWindows()
        return False

    return True


def wait_close_app():
    """
    Wait for the user to press the 'q' key or to close any of the windows
    """

    while True:
        if cv2.waitKey(1) == ord("q"):
            break

        # check if any window of the windows is closed
        if any(cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1 for window in WINDOW_LABELS):
            break

    cv2.destroyAllWindows()


DEFAULT_DETECTOR = Detector(
    families="tag25h9",
    nthreads=2,
    quad_decimate=2.0,
    quad_sigma=0.8,
    refine_edges=1,
    decode_sharpening=0.25,
)


def extract_tags_dict(image, detector=DEFAULT_DETECTOR) -> dict[int, list[Detection]]:
    """
    Extract tags from the given image using the given detector
    """

    tags: list[Detection] = detector.detect(image)

    tag_registry: dict[int, list[Detection]] = dict()

    for tag in tags:
        tag_id = tag.tag_id

        if tag_id not in tag_registry:
            tag_registry[tag_id] = []

        tag_registry[tag_id].append(tag)

    return tag_registry


def extract_tags_dict_single(image, detector=DEFAULT_DETECTOR) -> dict[int, Detection]:
    """
    Extract tags from the given image using the given detector and return only the first tag found for each tag id
    """

    tag_registry = extract_tags_dict(image, detector)

    return {tag_id: tags[0] for tag_id, tags in tag_registry.items()}


def extract_foreground(image):
    """
    Extracts the background from the given image and removes it, returning the normalized image
    """

    median_blur_size = 201

    bg_img = cv2.medianBlur(image, median_blur_size)

    # display_image("Background", bg_img)

    diff_img = 255 - cv2.absdiff(image, bg_img)

    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    return norm_img
