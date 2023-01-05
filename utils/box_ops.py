"""
This module contains utility functions for rotating boxes and
converting between different box representations.
"""

__all__ = (
    "box_cxcywh_to_4xy",
    "box_cxcywhr_to_4xy",
    "box_x1y1whr_to_bounding_cxcywh",
    "box_cxcywh_rel_to_abs",
    "box_cxcywhr_rel_to_abs",
    "box_cxcywh_abs_to_rel",
    "box_cxcywhr_abs_to_rel",
)

from math import sin, cos, radians


def box_cxcywh_to_4xy(cx, cy, w, h):
    """
    Converts a box from (`cx`, `cy`, `w`, `h`) format to
    (`x1`, `y1`, `x2`, `y2`, `x3`, `y3`, `x4`, `y4`)
    representation.
    """
    dx, dy = w / 2, h / 2
    x1, y1 = cx - dx, cy - dy
    x2, y2 = cx + dx, cy - dy
    x3, y3 = cx + dx, cy + dy
    x4, y4 = cx - dx, cy + dy
    return (x1, y1, x2, y2, x3, y3, x4, y4)


def box_cxcywhr_to_4xy(cx, cy, w, h, r, rad=False):
    """
    Converts a box from (`cx`, `cy`, `w`, `h`, `r`) format to
    (`x1`, `y1`, `x2`, `y2`, `x3`, `y3`, `x4`, `y4`)
    representation.
    """
    x1, y1, x2, y2, x3, y3, x4, y4 = box_cxcywh_to_4xy(cx, cy, w, h)
    x1, y1 = _rotate(cx, cy, x1, y1, r, rad)
    x2, y2 = _rotate(cx, cy, x2, y2, r, rad)
    x3, y3 = _rotate(cx, cy, x3, y3, r, rad)
    x4, y4 = _rotate(cx, cy, x4, y4, r, rad)
    return (x1, y1, x2, y2, x3, y3, x4, y4)


def box_x1y1whr_to_bounding_cxcywh(x1, y1, w, h, r, rad=False):
    """
    Compute the tightest rectangular bounding box
    (`cx`, `cy`, `w`, `h`) that bounds the rotated box
    (`x1`, `y1`, `w`, `h`, `r`).
    """
    x2, y2 = _rotate(x1, y1, x1 + w, y1, r, rad)
    x3, y3 = _rotate(x2, y2, x2, y2 + h, r, rad)
    x4, y4 = _rotate(x3, y3, x3 - w, y3, r, rad)

    cx, cy = _midpoint(x1, y1, x3, y3)
    xs = (x1, x2, x3, x4)
    ys = (y1, y2, y3, y4)
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)

    return (cx, cy, w, h)


def box_cxcywh_rel_to_abs(cx, cy, w, h, img_w, img_h):
    """
    Convert a box (`cx`, `cy`, `w`, `h`) from relative
    representation (percentage% relative to image size) to
    absolute.
    """
    cx = (cx / 100) * img_w
    cy = (cy / 100) * img_h
    w = (w / 100) * img_w
    h = (h / 100) * img_h
    return (cx, cy, w, h)


def box_cxcywhr_rel_to_abs(cx, cy, w, h, r, img_w, img_h):
    """
    Convert a box (`cx`, `cy`, `w`, `h`, `r`) from relative
    representation (percent% relative to image size) to
    absolute.
    """
    box = box_cxcywh_rel_to_abs(cx, cy, w, h, img_w, img_h)
    return (*box, r)


def box_cxcywh_abs_to_rel(cx, cy, w, h, img_w, img_h):
    """
    Convert a box (`cx`, `cy`, `w`, `h`) from absolute
    representation (pixels) to relative (percent%).
    """
    cx /= img_w
    cy /= img_h
    w /= img_w
    h /= img_h
    return (cx, cy, w, h)


def box_cxcywhr_abs_to_rel(cx, cy, w, h, r, img_w, img_h):
    """
    Convert a box (`cx`, `cy`, `w`, `h`, `r`) from absolute
    representation (pixels) to relative (percent%).
    """
    box = box_cxcywh_abs_to_rel(cx, cy, w, h, img_w, img_h)
    return (*box, r)


def _midpoint(x1, y1, x2, y2):
    """
    Computes the midpoint (`mx`, `my`) between two points
    (`x1`, `y1`) and (`x2`, `y2`).
    """
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (mx, my)


def _rotate(cx, cy, x, y, theta, rad=False):
    """
    Rotates point (`x`, `y`) about point (`cx`, `cy`) by
    angle `theta`. Returns the rotated point (`x1`, `y1`).
    """
    theta = radians(theta) if not rad else theta
    x1 = (x - cx) * cos(theta) - (y - cy) * sin(theta) + cx
    y1 = (x - cx) * sin(theta) + (y - cy) * cos(theta) + cy
    return (x1, y1)
