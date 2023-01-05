"""
Script to revert the image file names in a Label Studio Common
Format (JSON-MIN) file to the original path.
"""

__all__ = ("to_local_path",)

import re
from pathlib import Path


def to_local_path(path: Path | str, *, parent: Path | str = None) -> Path:
    """
    Get the image's local path from Label Studio Common Format
    (JSON-MIN) image path format.
    """
    try:
        filename = re.search(r"-([^.]+(\.[^.]+)?)$", str(path)).group(1)
    except AttributeError:
        raise ValueError(f"File name not found: {path}")
    filename = Path(filename)
    if parent is not None:
        filename = Path(parent) + filename
    return filename
