# OpenCV Maze Solver

<p align="center">
<img src="images/IMG_0867.jpg" width="300" />   
</p>

This is a simple maze solver using OpenCV and Python. The maze is solved using the A* algorithm from the NetworkX library.

## Installation

This project uses Poetry for dependency management. To install the dependencies, run the following command:

```bash
poetry install
```

## Usage

### Image

To run the maze solver, use the following command:

```bash
poetry run python main.py --image <image_path>
```

Replace `<image_path>` with the path to the maze image you want to solve like `images/IMG_0867.jpg`.


### Camera

To run the maze solver using the camera, use the following command:

```bash
poetry run python main_camera.py
```