import cv2
import numpy as np

import utils


def solve_maze(image, debug=False):
    original_width, original_height = image.shape[1], image.shape[0]
    image = cv2.resize(image, (4000, 3000))

    def debug_image(label, image, *args, **kwargs):
        if debug:
            utils.display_image(label, image, *args, **kwargs)

    debug_image("Image", image)

    # convert the image to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # extract the tags
    tag_registry = utils.extract_tags_dict_single(image_gray)

    missing_tags = {1, 2, 3, 4} - set(tag_registry.keys())
    if len(missing_tags) > 0:
        raise Exception(f"Missing tags in given image: {missing_tags}")

    # extract the foreground
    normalized_image = utils.extract_foreground(image_gray)
    debug_image("Normalized", normalized_image)

    # draw a black rectangle around the detected tags
    for r in tag_registry.values():
        (ptA, ptB, ptC, ptD) = r.corners

        # get min_x, min_y, max_x, max_y
        min_x = min(ptA[0], ptB[0], ptC[0], ptD[0])
        min_y = min(ptA[1], ptB[1], ptC[1], ptD[1])
        max_x = max(ptA[0], ptB[0], ptC[0], ptD[0])
        max_y = max(ptA[1], ptB[1], ptC[1], ptD[1])

        width = max_x - min_x
        height = max_y - min_y

        # enlarge the rectangle
        min_x -= (width / 7) * 1.5
        min_y -= (height * 2 / 7) * 1.5
        max_x += (width / 7) * 1.5
        max_y += (height / 7) * 1.5

        # draw the rectangle
        cv2.rectangle(normalized_image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (255, 255, 255), -1)

        # cv2.fillPoly(image, [np.int32(r.corners)], (0, 0, 0))

    # erode the image
    eroded = cv2.erode(normalized_image, np.ones((9, 9), np.uint8))
    # eroded = cv2.GaussianBlur(eroded, (15, 15), 0)

    debug_image("Eroded", eroded)

    # binarize the image
    _, thresh = cv2.threshold(eroded, 200, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)

    debug_image("Threshold", thresh)

    dilated = cv2.dilate(thresh, None, iterations=8)

    debug_image("Dilated", dilated)

    # crop the maze region using tag 1 and 2 as bounding box
    tag_1_center = tag_registry[1].center
    tag_2_center = tag_registry[2].center

    min_x = min(tag_1_center[0], tag_2_center[0])
    min_y = min(tag_1_center[1], tag_2_center[1])
    max_x = max(tag_1_center[0], tag_2_center[0])
    max_y = max(tag_1_center[1], tag_2_center[1])

    def transform_1(x, y):
        return x - min_x, y - min_y

    cropped_image = dilated[int(min_y) : int(max_y), int(min_x) : int(max_x)]

    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2BGR)

    cv2.circle(cropped_image, np.int32(transform_1(*tag_registry[3].center)), 10, (0, 0, 255), -1)
    cv2.circle(cropped_image, np.int32(transform_1(*tag_registry[4].center)), 10, (0, 255, 0), -1)

    debug_image("Cropped", cropped_image)

    def transform_2(x, y):
        return int((x - min_x) * 256 / (max_x - min_x)), int((y - min_y) * 256 / (max_y - min_y))

    maze_image_small = cv2.resize(cropped_image, (256, 256), interpolation=cv2.INTER_NEAREST)

    debug_image("Maze", maze_image_small, interpolation=cv2.INTER_NEAREST)

    # convert the maze image to a numpy bitmap

    maze_bitmap = np.zeros((256, 256), dtype=np.uint8)

    for x in range(256):
        for y in range(256):
            if maze_image_small[y, x, 0] > 0:
                maze_bitmap[y, x] = 1

    utils.display_image("Maze Bitmap", maze_bitmap * 255, interpolation=cv2.INTER_NEAREST)

    # use networkx to solve the maze

    import networkx as nx
    from networkx import Graph

    # def transform_3(x, y):
    #     pt = transform_2(x, y)
    #     return pt[0] // 2, pt[1] // 2

    G: Graph = nx.grid_2d_graph(256, 256)
    G.add_edges_from(
        [((x, y), (x + 1, y + 1)) for x in range(255) for y in range(255)]
        + [((x + 1, y), (x, y + 1)) for x in range(255) for y in range(255)],
        weight=1.4,
    )

    for x in range(256):
        for y in range(256):
            if maze_bitmap[y, x] == 1:
                G.remove_node((x, y))

    start_node = transform_2(*tag_registry[3].center)
    end_node = transform_2(*tag_registry[4].center)

    print(f"Start: {start_node}, End: {end_node}")

    def dist(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    try:
        path = nx.astar_path(G, start_node, end_node, heuristic=dist)
    except nx.NetworkXNoPath:
        raise Exception("No path found")

    print(f"Shortest path length: {len(path)}")

    # draw the path on the maze image
    for x, y in path:
        maze_image_small[y, x] = [0, 255, 0]

    debug_image("Maze Path", maze_image_small, interpolation=cv2.INTER_NEAREST)

    def un_transform(x, y):
        out_x = int(x * (max_x - min_x) / 256 + min_x)
        out_y = int(y * (max_y - min_y) / 256 + min_y)
        return int(out_x * original_width / 4000), int(out_y * original_height / 3000)

    path = [un_transform(x, y) for x, y in path]

    return path
