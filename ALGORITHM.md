# Algorithm Explanation

1. **Load**. 

    First we load the image

    <img src="debug-steps/001_Image_w500.png" alt="step 1 - image" width="500">

2. **Normalization**.

    The we use a median blur to extract the background and then remove it from the image. Then we normalize the image.

    <img src="debug-steps/002_Normalized_w500.png" alt="step 2 - normalized" width="500">

3. **Erosion**.

    Then we draw some white rectangles over all the markers to hide them as they would occlude the maze. Then we erode the image to remove noise and make the maze lines thicker.

    <img src="debug-steps/003_Eroded_w500.png" alt="step 3 - eroded" width="500">

4. **Threshold**.

    Now we binarize the image using a threshold (a good number I found is about ~200)

    <img src="debug-steps/004_Threshold_w500.png" alt="step 4 - threshold" width="500">

5. **Dilate**.

    Then we dilate the image to make the lines even thicker.

    <img src="debug-steps/005_Dilated_w500.png" alt="step 5 - dilated" width="500">

6. **Cropping**.

    We crop the image using markers 1 and 2 to get the maze region.

    <img src="debug-steps/006_Cropped_w500.png" alt="step 6 - cropped" width="500">

7. **Maze**.

    We draw the maze with the start (red) and end (green) points in the new coordinates.

    <img src="debug-steps/007_Maze_w500.png" alt="step 7 - maze" width="500">

8. **Bitmap**.

    We create a bitmap of the maze to use it in the A* algorithm. The bitmap is a 2D array where 0 is a free cell and 1 is a wall. We use networkx to run the A* algorithm.

    <img src="debug-steps/008_Maze Bitmap_w500.png" alt="step 8 - maze bitmap" width="500">

9. **Path**.

    We draw the path found by the A* algorithm on the maze bitmap.

    <img src="debug-steps/009_Maze Path_w500.png" alt="step 9 - maze path" width="500">

10. **Solution**.

    Finally we transform the path back to the original image coordinates and draw it on the image.

    <img src="debug-steps/010_Solution_w500.png" alt="step 10 - solution" width="500">

