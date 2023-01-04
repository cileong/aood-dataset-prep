# Scripts for Barcode Detection Dataset Preparation

Note that the dataset is unreleased, and we have no plans on releasing it (yet).

## Introduction

The raw dataset annotations are encoded in [Label Studio](https://labelstud.io) Common Format, and are expected to be converted to a COCO-like format before publication.

The preprocessed COCO-like annotation should conform to the following structure:

```
{
  "images": [
    {
      "id": Integer,
      "file_name": String,
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
