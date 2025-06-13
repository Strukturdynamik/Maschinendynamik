import math
import numpy as np
from ipycanvas import hold_canvas

"""
This file is based on code from nrsyed/utilities: https://github.com/nrsyed/utilities/blob/master/spring/spring.py
Original author: nrsyed
License: GNU General Public License v3.0 (GPL-3.0)

This version may contain modifications. It is distributed under the same GPL-3.0 license.

See LICENSE file for details.
"""


def spring(start, end, nodes, width):
    """!
    Return a list of points corresponding to a spring. For details on the use see:
    https://github.com/nrsyed/utilities/blob/master/spring/README.md

    @param r1 (array-like) The (x, y) coordinates of the first endpoint.
    @param r2 (array-like) The (x, y) coordinates of the second endpoint.
    @param nodes (int) The number of spring "nodes" or coils.
    @param width (int or float) The diameter of the spring.
    @return An array of x coordinates and an array of y coordinates.
    """

    # Check that nodes is at least 1.
    nodes = max(int(nodes), 1)

    # Convert to numpy array to account for inputs of different types/shapes.
    start, end = np.array(start).reshape((2,)), np.array(end).reshape((2,))

    # If both points are coincident, return the x and y coords of one of them.
    if (start == end).all():
        return start[0], start[1]

    # Calculate length of spring (distance between endpoints).
    length = np.linalg.norm(np.subtract(end, start))

    # Calculate unit vectors tangent (u_t) and normal (u_t) to spring.
    u_t = np.subtract(end, start) / length
    u_n = np.array([[0, -1], [1, 0]]).dot(u_t)

    # Initialize array of x (row 0) and y (row 1) coords of the nodes+2 points.
    spring_coords = np.zeros((2, nodes + 2))
    spring_coords[:, 0], spring_coords[:, -1] = start, end

    # Check that length is not greater than the total length the spring
    # can extend (otherwise, math domain error will result), and compute the
    # normal distance from the centerline of the spring.
    normal_dist = math.sqrt(max(0, width**2 - (length**2 / nodes**2))) / 2

    # Compute the coordinates of each point (each node).
    for i in range(1, nodes + 1):
        spring_coords[:, i] = (
            start
            + ((length * (2 * i - 1) * u_t) / (2 * nodes))
            + (normal_dist * (-1) ** i * u_n)
        )

    return spring_coords[0, :], spring_coords[1, :]


def draw_spring(
    canvas,
    x_coords,
    y_coords,
    spring_anker_point,
    width_offset,
    height_offset,
    clear_x,
    clear_y,
):
    """Function to draw a spring.

    Args:
        canvas (Canvas): Canvas that is drawn on.
        x_coords (np.array): X coordinates that form the spring.
        y_coords (np.array): Y coordinates that form the spring.
        spring_anker_point (tuple(int, int)): Point where the spring is
            attached.
        width_offset (int): Offset.
        height_offset (int): Offset.
        clear_x (int): Size of canvas to clear it.
        clear_y (int): Size of canvas to clear it.
    """
    with hold_canvas():
        canvas.clear_rect(
            clear_x,
            clear_y,
            canvas.width,
            canvas.height,
        )
        if np.isscalar(x_coords):
            canvas.stroke_line(
                spring_anker_point[0] + width_offset,
                spring_anker_point[1] - height_offset,
                x_coords,
                y_coords,
            )
            canvas.stroke_line(
                x_coords,
                y_coords,
                x_coords,
                y_coords,
            )
        else:
            canvas.stroke_lines(list(zip(x_coords, y_coords)))
            index = len(x_coords) - 1
            canvas.stroke_line(
                x_coords[index],
                y_coords[index],
                x_coords[index],
                y_coords[index],
            )
