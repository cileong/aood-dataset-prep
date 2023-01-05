"""
Converter that converts data from Label Studio Common Format
(JSON-MIN) to a COCO-like format, tailored for the arbitrary-
oriented object detection task.
"""

__all__ = ("DataConverter",)

from PIL import Image, ImageOps

import json
from pathlib import Path

from utils.box_ops import box_x1y1whr_to_bounding_cxcywh


class DataConverter:
    """
    Converter that converts data from Label Studio Common Format
    (JSON-MIN) to a COCO-like format, tailored for the arbitrary-
    oriented object detection task.

    Read the repository README for the target structure.

    Note: requires the dataset images to be present.
    """

    __slots__ = "_images", "_categories", "_annotations"

    def __init__(self, data: list) -> None:
        """
        Initialize a CocoLikeData object from dictionary in
        Label Studio Common Format.

        Args:
            data (dict): Dictionary with JSON-MIN structure.
        """
        assert isinstance(data, list), "Input is not a list."

        images: list[dict] = []
        categories: dict[str, int] = {}
        annotations: list[dict] = []

        for entry in data:

            img_id, filename, img_width, img_height = DataConverter._get_image(entry)
            images.append(
                {
                    "id": img_id,
                    "file_name": filename,
                    "width": img_width,
                    "height": img_height,
                }
            )

            for label in entry["label"]:

                # Assuming this is a single-class detection task.
                # Map category name to category ID.
                (cat_name,) = label["rectanglelabels"]
                if cat_name not in categories:
                    cat_id = len(categories) + 1
                    categories[cat_name] = cat_id

                x1 = label["x"]
                y1 = label["y"]
                w = label["width"]
                h = label["height"]
                r = label["rotation"]
                cx, cy, *_ = box_x1y1whr_to_bounding_cxcywh(x1, y1, w, h, r)
                annotations.append(
                    {
                        "id": len(annotations),
                        "image_id": img_id,
                        "category_id": cat_id,
                        "bbox": [cx, cy, w, h],
                        "rotation": r,
                        "area": w * h,
                    }
                )

        self._images: list[dict] = images
        self._categories: list[dict] = [
            {"id": cat_id, "name": cat_name} for cat_name, cat_id in categories.items()
        ]
        self._annotations: list[dict] = annotations

    @classmethod
    def from_json(cls, path: Path | str) -> "DataConverter":
        """
        Initialize a CocoLikeData object from a JSON file in
        Label Studio Common Format.

        Args:
            data (dict): Path to a JSON file with JSON-MIN
                structure.
        """
        with open(path) as file:
            data = json.load(file)
        return cls(data)

    def to_dict(self) -> dict:
        """
        Convert the stored data to a dictionary.
        """
        return {
            "images": self.images,
            "categories": self.categories,
            "annotations": self.annotations,
        }

    def to_json(self, path: Path | str) -> None:
        """
        Serialize the stored data to a JSON file.

        Args:
            path (Path | str): Path to the JSON file.
        """
        with open(path, "w") as file:
            json.dump(self.to_dict(), file)

    @staticmethod
    def _get_image(entry: dict) -> tuple[int, str, int, int]:
        """
        Get the image data from the entry.

        Args:
            entry (dict): An entry of JSON-MIN structure.
        """
        img_id = entry["id"]
        filename = entry["image"]
        with Image.open(filename) as img:
            img = ImageOps.exif_transpose(img)
            width, height = map(int, img.size)
        return img_id, filename, width, height

    @property
    def images(self) -> list[dict]:
        """The list of image data."""
        return self._images

    @property
    def categories(self) -> list[dict]:
        """The list of categories."""
        return self._categories

    @property
    def annotations(self) -> list[dict]:
        """The list of annotations (across images)."""
        return self._annotations
