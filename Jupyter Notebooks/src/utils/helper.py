from typing import Tuple, Any
import copy
import math
from ipycanvas import Canvas, hold_canvas
from ..utils.constants import DIRECTIONS

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
    return mapped_value


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
        canvas (Canvas): Canvas that is drawn on.
        pos (Tuple[int, int]): Position where text is animated.
        font_size (int): Font size of text.
        max_width (int): Max width of text.
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


def rotate_point(x, y, pivot_x, pivot_y, angle):
    """Rotate a point (x, y) around a pivot by angle (in degrees).

    Args:
        x (int): X value of rotated position.
        y (int): Y value of rotated position.
        pivot_x (int): X value of pivot position.
        pivot_y (int): Y value of rotated position.
        angle (int): Angle of rotation.

    Returns:
        tuple(int, int): Rotated position (x, y).
    """
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
    if direction == "vertical":
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
        daempfer_middle = [fork_right[0], fork_right[1] + daempfer_fork_extension]
        daempfer_left = [
            fork_right[0] - daempfer_fork_width / 2,
            fork_right[1] + daempfer_fork_extension,
        ]
        daempfer_right = [
            fork_right[0] + daempfer_fork_width / 2,
            fork_right[1] + daempfer_fork_extension,
        ]
        daempfer_bottom_left = [
            daempfer_left[0],
            daempfer_left[1] + daempfer_fork_length,
        ]
        daempfer_bottom_right = [
            daempfer_right[0],
            daempfer_right[1] + daempfer_fork_length,
        ]
        spring_anker_point = fork_left
    elif direction == "left_to_right":
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
        spring_anker_point = fork_left
    elif direction == "right_to_left":
        # fork_left = [
        #     anker_point_top[0] - anker_point_extension,
        #     anker_point_top[1] - fork_width / 2,
        # ]
        # fork_right = [
        #     anker_point_top[0] - anker_point_extension,
        #     anker_point_top[1] + fork_width / 2,
        # ]
        # fork_middle = [
        #     anker_point_top[0] - anker_point_extension,
        #     anker_point_top[1],
        # ]
        # daempfer_middle = [fork_left[0], fork_left[1] - daempfer_fork_extension]
        # daempfer_left = [
        #     fork_left[0] - daempfer_fork_extension,
        #     fork_left[1] - daempfer_fork_width / 2,
        # ]
        # daempfer_right = [
        #     fork_left[0] - daempfer_fork_extension,
        #     fork_left[1] + daempfer_fork_width / 2,
        # ]
        # daempfer_bottom_left = [
        #     daempfer_left[0] - daempfer_fork_length,
        #     daempfer_left[1],
        # ]
        # daempfer_bottom_right = [
        #     daempfer_right[0] - daempfer_fork_length,
        #     daempfer_right[1],
        # ]
        # spring_anker_point = fork_right
        raise NotImplementedError("Not implemented yet")
    else:
        raise ValueError(
            "Invalid direction. Choose from 'vertical', 'left_to_right', or 'right_to_left'."
        )

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
    if direction == "left_to_right":
        bottom_fork_middle = [
            anker_point_bottom[0] - bottom_fork_extension,
            anker_point_bottom[1],
        ]
    elif direction == "right_to_left":
        bottom_fork_middle = [
            anker_point_bottom[0] + bottom_fork_extension,
            anker_point_bottom[1],
        ]
    elif direction == "vertical":
        bottom_fork_middle = [
            anker_point_bottom[0],
            anker_point_bottom[1] - bottom_fork_extension,
        ]
    else:
        raise ValueError(
            "Invalid direction. Choose from 'left_to_right', 'right_to_left', or 'vertical'."
        )

    canvas.stroke_line(
        anker_point_bottom[0],
        anker_point_bottom[1],
        bottom_fork_middle[0],
        bottom_fork_middle[1],
    )

    if direction in ["left_to_right", "right_to_left"]:
        bottom_fork_right = [
            bottom_fork_middle[0],
            bottom_fork_middle[1] - bottom_fork_width / 2,
        ]
        bottom_fork_left = [
            bottom_fork_middle[0],
            bottom_fork_middle[1] + bottom_fork_width / 2,
        ]
    else:  # vertical
        bottom_fork_right = [
            bottom_fork_middle[0] - bottom_fork_width / 2,
            bottom_fork_middle[1],
        ]
        bottom_fork_left = [
            bottom_fork_middle[0] + bottom_fork_width / 2,
            bottom_fork_middle[1],
        ]

    canvas.stroke_line(
        bottom_fork_right[0],
        bottom_fork_right[1],
        bottom_fork_left[0],
        bottom_fork_left[1],
    )

    if direction == "left_to_right":
        daempfer_middle = [bottom_fork_left[0] - daempfer_length, bottom_fork_left[1]]
    elif direction == "right_to_left":
        daempfer_middle = [bottom_fork_left[0] + daempfer_length, bottom_fork_left[1]]
    else:  # vertical
        daempfer_middle = [bottom_fork_left[0], bottom_fork_left[1] - daempfer_length]

    if direction in ["left_to_right", "right_to_left"]:
        daempfer_left = [daempfer_middle[0], daempfer_middle[1] + daempfer_width / 2]
        daempfer_right = [daempfer_middle[0], daempfer_middle[1] - daempfer_width / 2]
    else:  # vertical
        daempfer_left = [daempfer_middle[0] - daempfer_width / 2, daempfer_middle[1]]
        daempfer_right = [daempfer_middle[0] + daempfer_width / 2, daempfer_middle[1]]

    canvas.stroke_line(
        bottom_fork_left[0],
        bottom_fork_left[1],
        daempfer_middle[0],
        daempfer_middle[1],
    )
    canvas.stroke_line(
        daempfer_left[0], daempfer_left[1], daempfer_right[0], daempfer_right[1]
    )

    return (
        bottom_fork_right
        if direction in ["left_to_right", "right_to_left"]
        else bottom_fork_right
    )


def draw_line_with_strokes(
    canvas: Canvas,
    x_1: int,
    y_1: int,
    x_2: int,
    y_2: int,
    len_strokes: int,
    num_strokes: int,
    angle: int,
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
        angle (int): Angle of strokes
            Note: currently the angle can mess with the direction
            of the strokes. Adjust accordingly.
        direction_strokes (str): Direction of the strokes.
            "top", "bottom", "left" or "right".
    """
    # draw line
    canvas.stroke_line(x1=x_1, y1=y_1, x2=x_2, y2=y_2)

    # angles and offset for strokes
    x_offset = len_strokes * math.sin(math.radians(angle))
    y_offset = len_strokes * math.cos(math.radians(angle))

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
    canvas,
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
    """Function to draw an horizontal arrow with a base and optional description.

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

    # angle of the arrow shaft
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_angle_rad = math.radians(arrow_angle)

    # arrowhead lines
    x3 = x2 - arrow_length * math.cos(angle - arrow_angle_rad)
    y3 = y2 - arrow_length * math.sin(angle - arrow_angle_rad)
    x4 = x2 - arrow_length * math.cos(angle + arrow_angle_rad)
    y4 = y2 - arrow_length * math.sin(angle + arrow_angle_rad)

    canvas.stroke_line(x2, y2, x3, y3)
    canvas.stroke_line(x2, y2, x4, y4)

    if base_length is not None:
        # Calculate perpendicular vector to arrow shaft
        perp_angle = angle + math.pi / 2  # rotate 90°
        half_base = base_length / 2
        base_start_x = x1 + half_base * math.cos(perp_angle)
        base_start_y = y1 + half_base * math.sin(perp_angle)
        base_end_x = x1 - half_base * math.cos(perp_angle)
        base_end_y = y1 - half_base * math.sin(perp_angle)

        # Draw base line
        canvas.stroke_line(base_start_x, base_start_y, base_end_x, base_end_y)

        # Add angled strokes
        if num_base_strokes and stroke_len:
            total_length = base_length
            stroke_spacing = total_length / num_base_strokes + (spacing_padding or 0)

            # unit vector along base line
            dx = (base_end_x - base_start_x) / total_length
            dy = (base_end_y - base_start_y) / total_length

            # unit vector for angled stroke (same angle as alpha, rotated from perpendicular)
            alpha_rad = math.radians(alpha)
            stroke_dx = stroke_len * math.cos(angle - alpha_rad)
            stroke_dy = stroke_len * math.sin(angle - alpha_rad)

            for i in range(num_base_strokes):
                px = base_start_x + i * stroke_spacing * dx
                py = base_start_y + i * stroke_spacing * dy
                canvas.stroke_line(px, py, px - stroke_dx, py - stroke_dy)

    # Draw description
    if description is not None:
        offset_x = abs_value(canvas.width, description_padding_x)
        offset_y = abs_value(canvas.height, description_padding_y)

        # place the text relative to the start point, perpendicular to arrow direction
        perp_angle = angle + math.pi / 2
        text_x = x1 + offset_x * math.cos(perp_angle)
        text_y = y1 + offset_y * math.sin(perp_angle)

        canvas.line_width = 0.9
        canvas.font = f"{description_style} {abs_value(canvas.width, description_font_size)}px euklid"
        canvas.fill_text(
            description,
            text_x,
            text_y,
            max_width=abs_value(canvas.width, description_max_width),
        )
