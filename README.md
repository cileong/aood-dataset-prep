# Arbitrary-Oriented Object Detection - Dataset Preparation Tools

## Introduction

At the moment, the tools in this repository only support conversion *from* the [Label Studio](https://labelstud.io) Common Format.

The script will convert the dataset annotations to a COCO-like format with the following structure:

```
{
  "images": [
    {
      "id": Integer,
      "filename": String,
      "width": Integer,
      "height": Integer
    }
  ],
  "categories": [
    {
      "id": Integer,
      "name": String
    }
  ],
  "annotations": [
    {
      "id": Integer,
      "image_id": Integer,
      "category_id": Integer,
      "bbox": [
        cx: Float,
        cy: Float,
        w: Float,
        h: Float
      ],
      "rotation": Float
    }
  ]
}
```

More target formats and other functionalities may be added in the future upon request.
