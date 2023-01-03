# Scripts for Barcode Detection Dataset Preparation

## Introduction

The raw dataset annotations are in Label Studio Common Format, and are expected to be converted to a COCO-like format before publication.

The preprocessed COCO-like annotation should conform to the following structure:

```json
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

The scripts in the repository encode the annotations into the COCO-like format.
