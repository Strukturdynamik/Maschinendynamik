from typing import Tuple, Any
import copy
import math
from ipycanvas import Canvas, hold_canvas
import numpy as np

from ..utils.constants import DIRECTIONS  # , DIRECTION_FDE

"""Modules containing helper functions.
"""


def abs_value(whole: int, percentage: int) -> int:
    """Function to calculate the actual value given
        a percentage and a whole.

    Args:
        whole (int): Whole.
        percentage (int): Percentage.

    Returns:
        int: Actual value.
    """

    return int((percentage / 100) * whole)


def calculate_percentage(value: int, whole: int) -> int:
    """Function to calculate the percentage given
        a percentage and a whole.

    Args:
        value (int): Actual value.
        whole (int): Whole.

    Raises:
        NotImplementedError: _description_

    Returns:
        int: Percentage.
    """
    if whole == 0:
        raise NotImplementedError
    return int(value / whole) * 100


def map_value(
    value: int, original_min: int, original_max: int, target_min: int, target_max: int
) -> float:
    """Function to map a value form original domain to target domain.

    Args:
        value (int): Value to map.
        original_min (int): Lower bound of original domain.
        original_max (int): Upper bound of original domain.
        target_min (int): Lower bound of target domain.
        target_max (int): Upper bound of target domain.

    Raises:
        ValueError: _description_

    Returns:
        int: Mapped value.
    """
    # check for zero range to avoid division by zero
    if original_min == original_max:
        raise ValueError("The original range cannot be zero.")

    # calculate the mapped value
    mapped_value = (value - original_min) / (original_max - original_min) * (
        target_max - target_min
    ) + target_min
    return mapped_value  # int(mapped_value)


def animate_text(
    canvas: Canvas,
    pos: Tuple[int, int],
    text: str,
    font_size: int,
    font_style: str,
    max_width: int,
    fill_style: str,
    x_padding: int,
    y_padding: int,
) -> None:
    """Function to draw/animate text at a specific location.

    Args:
        canvas (Canvas): _description_
        pos (Tuple[int, int]): _description_
        font_size (int): _description_
        max_width (int): _description_
    """
    with hold_canvas():
        canvas.clear()
        canvas.fill_style = fill_style
        canvas.font_style = f"{font_style}"
        canvas.font = f"{abs_value(canvas.width, font_size)}px euklid"
        max_width = abs_value(canvas.width, max_width)
        canvas.fill_text(
            text,
            x=pos[0] + abs_value(canvas.width, x_padding),
            y=pos[1] + abs_value(canvas.width, y_padding),
            max_width=max_width,
        )


def calc_dummy_solution(spring_anker_point):
    x = np.linspace(0, 1 * np.pi, 100)
    y = list(np.sin(0.2 * x) * 100 + 1.1)
    pos_vec = [(spring_anker_point[0] + 10, spring_anker_point[1])]
    for val in y:
        pos_vec.append((spring_anker_point[0] + 10 + int(val), spring_anker_point[1]))
    return pos_vec


def draw_line_with_strokes(
    canvas: Canvas,
    x_1: int,
    y_1: int,
    x_2: int,
    y_2: int,
    len_strokes: int,
    num_strokes: int,
    alpha: int,
    direction_strokes: str,
):
    """Function to draw line with strokes.

    Args:
        canvas (Canvas): Canvas to draw on.
        x_1 (int): X1.
        y_1 (int): Y1.
        x_2 (int): X2.
        y_2 (int): Y2.
        len_strokes (int): Length of strokes.
        num_strokes (int): Number of strokes.
        alpha (int): Angle of strokes
            Note: currently the angle can mess with the direction
            of the strokes. Adjust accordingly.
        direction_strokes (str): Direction of the strokes.
            "top", "bottom", "left" or "right".
    """
    # draw line
    canvas.stroke_line(x1=x_1, y1=y_1, x2=x_2, y2=y_2)

    # angles and offset for strokes
    x_offset = len_strokes * math.sin(math.radians(alpha))
    y_offset = len_strokes * math.cos(math.radians(alpha))

    # draw strokes
    # canvas.line_width = 0.5
    direction = DIRECTIONS[f"{direction_strokes}"]
    counter = 0
    # split into cases
    temp_start = [copy.deepcopy(x_1), copy.deepcopy(y_1)]

    if direction_strokes == "top" or direction_strokes == "bottom":
        # space between strokes
        stroke_space = (x_2 - x_1) / num_strokes
        # vertical line
        while counter < num_strokes and temp_start[0] < x_2:
            canvas.stroke_line(
                temp_start[0],
                temp_start[1],
                temp_start[0] + direction[0] * x_offset,
                temp_start[1] + direction[1] * y_offset,
            )
            counter += 1
            temp_start[0] = temp_start[0] + stroke_space

    else:
        # space between strokes
        stroke_space = (y_2 - y_1) / num_strokes
        # vertical line
        while counter < num_strokes and temp_start[1] < y_2:
            canvas.stroke_line(
                temp_start[0],
                temp_start[1],
                temp_start[0] + direction[0] * x_offset,
                temp_start[1] + direction[1] * y_offset,
            )
            counter += 1
            temp_start[1] = temp_start[1] + stroke_space


def draw_arrow(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    alpha: int = 30,
    arrow_length: int = 15,
    arrow_angle: int = 30,
    base_length: int | Any = None,
    num_base_strokes: int | Any = None,
    stroke_len: int | Any = None,
    spacing_padding: int | Any = None,
    description: str | Any = None,
    description_font_size: int | Any = None,
    description_style: str | Any = None,
    description_max_width: int | Any = None,
    description_padding_x: int | Any = None,
    description_padding_y: int | Any = None,
):
    """Function to draw an arrow with a base and optional description.

    Args:
        canvas (Canvas): Canvas to draw on.
        x1 (int): X value of arrow starting point.
        y1 (int): Y value of arrow starting point.
        x2 (int): X value of arrow end point.
        y2 (int): Y value of arrow end point.
        alpha (int, optional): Angle of strokes. Defaults to 30.
        arrow_length (int, optional): Length of arrow tip. Defaults to 15.
        arrow_angle (int, optional): Angle of arrow tip. Defaults to 30.
        base_length (int): Length of arrow base.
        num_base_strokes (int, optional): Number of strokes
            on arrow base. Defaults to 4.
        stroke_len (int, optional): Length of strokes
            on arrow base. Defaults to 5.
        spacing_padding (int, optional): Padding to increase space between
             strokes. Defaults to 5.
        description (str | Any, optional): Description of arrow. Defaults to None.
        description_font_size (int | Any, optional): Description font size. Must
            be passed as percentage of canvas.width or canvas.height. Defaults to None.
        description_style (str | Any, optional): Style of description. Defaults to None.
        description_max_width (int | Any, optional): Max width of description.
            Must be passed as percentage of canvas.width or canvas.height.
            Defaults to None.
        description_padding_x (int | Any, optional): Padding on starting point of
            arrow. Defaults to None.
        description_padding_y (int | Any, optional): Padding to put description
            slightly above arrow. Defaults to None.

    Raises:
        NotImplementedError: _description_
    """

    # draw main line
    canvas.stroke_line(x1, y1, x2, y2)

    # calculate the angle of the line
    angle = math.atan2(y2 - y1, x2 - x1)

    # calculate coordinates for the two arrowhead lines
    arrow_angle_rad = math.radians(arrow_angle)

    x3 = x2 - arrow_length * math.cos(angle - arrow_angle_rad)
    y3 = y2 - arrow_length * math.sin(angle - arrow_angle_rad)

    x4 = x2 - arrow_length * math.cos(angle + arrow_angle_rad)
    y4 = y2 - arrow_length * math.sin(angle + arrow_angle_rad)

    # strke arrow head lines
    canvas.stroke_line(x2, y2, x3, y3)
    canvas.stroke_line(x2, y2, x4, y4)

    if base_length is not None:
        # draw base line
        canvas.stroke_line(x1, y1 - base_length / 2, x1, y1 + base_length / 2)

        # add angled lines
        line_space = math.ceil(base_length / num_base_strokes) + spacing_padding
        gamma = 90
        beta = 180 - 90 - alpha
        if alpha + beta + gamma != 180:
            raise NotImplementedError("alpha beta and gamma dont add up to 180")
        # calculate y axis offset
        y_offset = -(stroke_len / math.sin(gamma)) * math.sin(
            alpha
        )  # a = (c/sin(gamma))*sin(alpha)
        # calculate x axis offset
        x_offset = -(stroke_len / math.sin(gamma)) * math.sin(
            beta
        )  # b = (c/sin(gamma))*sin(beta)

        temp_start = (x1, y1 - base_length / 2)
        counter = 0
        while (
            counter
            < num_base_strokes  # temp_start[1] < y1 - base_length / 2 + base_length and
        ):
            canvas.stroke_line(
                temp_start[0],
                temp_start[1],
                temp_start[0] - x_offset,
                temp_start[1] - y_offset,
            )
            temp_start = (temp_start[0], temp_start[1] + line_space)
            counter += 1

    # if arrow has description add it
    if description is not None:
        center = (
            x1 + abs_value(canvas.width, description_padding_x),
            y1 - abs_value(canvas.height, description_padding_y),
        )
        canvas.line_width = 0.9
        canvas.font = f"{description_style} {abs_value(canvas.width, description_font_size)}px euklid"
        canvas.fill_text(
            description,
            center[0],
            center[1],
            max_width=abs_value(canvas.width, description_max_width),
        )


def rotate_point(x, y, pivot_x, pivot_y, angle):
    """Rotate a point (x, y) around a pivot by angle (in degrees)."""
    x_new = pivot_x + (x - pivot_x) * math.cos(angle) - (y - pivot_y) * math.sin(angle)
    y_new = pivot_y + (x - pivot_x) * math.sin(angle) + (y - pivot_y) * math.cos(angle)
    return x_new, y_new


def ghetto_feder_daempfer_element_top(
    canvas,
    anker_point_top,
    fork_width,
    anker_point_extension,
    daempfer_fork_extension,
    daempfer_fork_length,
    daempfer_fork_width,
    direction,
):
    """Draw ghetto feder daempfer element.

    Args:
        canvas (_type_): _description_
        anker_point (_type_): _description_
        fork_width (_type_): _description_
        anker_point_extension (_type_): _description_
        daempfer_fork_extension (_type_): _description_
        daempfer_fork_length (_type_): _description_
        daempfer_fork_width (_type_): _description_
        direction (_type_): "vertical", "left_to_right"

    Returns:
        _type_: _description_
    """

    if direction == "vertical":
        # upper fork
        fork_left = [
            anker_point_top[0] - fork_width / 2,
            anker_point_top[1] + anker_point_extension,
        ]
        fork_right = [
            anker_point_top[0] + fork_width / 2,
            anker_point_top[1] + anker_point_extension,
        ]
        fork_middle = [
            anker_point_top[0],
            anker_point_top[1] + anker_point_extension,
        ]

        # daempfer fork
        daempfer_middle = [fork_left[0], fork_left[1] + daempfer_fork_extension]
        daempfer_left = [
            fork_left[0] - daempfer_fork_width / 2,
            fork_left[1] + daempfer_fork_extension,
        ]
        daempfer_right = [
            fork_left[0] + daempfer_fork_width / 2,
            fork_left[1] + daempfer_fork_extension,
        ]
        daempfer_bottom_left = [
            daempfer_left[0],
            daempfer_left[1] + daempfer_fork_length,
        ]
        daempfer_bottom_right = [
            daempfer_right[0],
            daempfer_right[1] + daempfer_fork_length,
        ]

        # set spring ankerpoint
        spring_anker_point = fork_right

        # draw all lines
        canvas.stroke_line(
            anker_point_top[0], anker_point_top[1], fork_middle[0], fork_middle[1]
        )
        canvas.stroke_line(fork_left[0], fork_left[1], fork_right[0], fork_right[1])
        canvas.stroke_line(
            fork_left[0], fork_left[1], daempfer_middle[0], daempfer_middle[1]
        )
        canvas.stroke_line(
            daempfer_left[0], daempfer_left[1], daempfer_right[0], daempfer_right[1]
        )
        canvas.stroke_line(
            daempfer_left[0],
            daempfer_left[1],
            daempfer_bottom_left[0],
            daempfer_bottom_left[1],
        )
        canvas.stroke_line(
            daempfer_right[0],
            daempfer_right[1],
            daempfer_bottom_right[0],
            daempfer_bottom_right[1],
        )

    else:
        if direction == "left_to_right":
            # upper fork
            fork_left = [
                anker_point_top[0] + anker_point_extension,
                anker_point_top[1] - fork_width / 2,
            ]
            fork_right = [
                anker_point_top[0] + anker_point_extension,
                anker_point_top[1] + fork_width / 2,
            ]
            fork_middle = [
                anker_point_top[0] + anker_point_extension,
                anker_point_top[1],
            ]

            # daempfer fork
            daempfer_middle = [fork_right[0] + daempfer_fork_extension, fork_right[1]]
            daempfer_left = [
                fork_right[0] + daempfer_fork_extension,
                fork_right[1] - daempfer_fork_width / 2,
            ]
            daempfer_right = [
                fork_right[0] + daempfer_fork_extension,
                fork_right[1] + daempfer_fork_width / 2,
            ]
            daempfer_bottom_left = [
                daempfer_left[0] + daempfer_fork_length,
                daempfer_left[1],
            ]
            daempfer_bottom_right = [
                daempfer_right[0] + daempfer_fork_length,
                daempfer_right[1],
            ]

            # set spring ankerpoint
            spring_anker_point = fork_left

            # draw upper fork
            canvas.stroke_line(
                anker_point_top[0], anker_point_top[1], fork_middle[0], fork_middle[1]
            )
            canvas.stroke_line(fork_left[0], fork_left[1], fork_right[0], fork_right[1])
            canvas.stroke_line(
                fork_right[0], fork_right[1], daempfer_middle[0], daempfer_middle[1]
            )
            canvas.stroke_line(
                daempfer_left[0], daempfer_left[1], daempfer_right[0], daempfer_right[1]
            )
            canvas.stroke_line(
                daempfer_left[0],
                daempfer_left[1],
                daempfer_bottom_left[0],
                daempfer_bottom_left[1],
            )
            canvas.stroke_line(
                daempfer_right[0],
                daempfer_right[1],
                daempfer_bottom_right[0],
                daempfer_bottom_right[1],
            )
        else:
            if "right_to_left":
                raise NotImplementedError("Not implemented yet")

    return spring_anker_point


def ghetto_feder_daempfer_element_bottom(
    canvas,
    anker_point_bottom,
    bottom_fork_extension,
    bottom_fork_width,
    daempfer_length,
    daempfer_width,
    direction,
):
    # lower fork
    # make the bottom part of feder daempfer element

    if direction == "left_to_right":
        bottom_fork_middle = [
            anker_point_bottom[0] - bottom_fork_extension,
            anker_point_bottom[1],
        ]
        canvas.stroke_line(
            anker_point_bottom[0],
            anker_point_bottom[1],
            bottom_fork_middle[0],
            bottom_fork_middle[1],
        )

        bottom_fork_right = [
            bottom_fork_middle[0],
            bottom_fork_middle[1] - bottom_fork_width / 2,
        ]
        bottom_fork_left = [
            bottom_fork_middle[0],
            bottom_fork_middle[1] + bottom_fork_width / 2,
        ]
        canvas.stroke_line(
            bottom_fork_right[0],
            bottom_fork_right[1],
            bottom_fork_left[0],
            bottom_fork_left[1],
        )

        daempfer_middle = [bottom_fork_left[0] - daempfer_length, bottom_fork_left[1]]
        daempfer_left = [daempfer_middle[0], daempfer_middle[1] + daempfer_width / 2]
        daempfer_right = [daempfer_middle[0], daempfer_middle[1] - daempfer_width / 2]
        canvas.stroke_line(
            bottom_fork_left[0],
            bottom_fork_left[1],
            daempfer_middle[0],
            daempfer_middle[1],
        )
        canvas.stroke_line(
            daempfer_left[0], daempfer_left[1], daempfer_right[0], daempfer_right[1]
        )

        spring_anker_point_bottom = bottom_fork_right

    else:
        if direction == "vertical":
            raise NotImplementedError("Not implemented yet")

        else:

            if direction == "right_to_left":
                raise NotImplementedError("Not implemented yet")

    return spring_anker_point_bottom
