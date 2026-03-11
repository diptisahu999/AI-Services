import cv2
import os
from pathlib import Path

class ImageToArtService:
    @staticmethod
    def process(input_path: str | Path, output_path: str | Path):
        """
        Processes an image to create a pencil sketch (art) effect.
        """
        image = cv2.imread(str(input_path))
        if image is None:
            raise FileNotFoundError(f"Could not load image from {input_path}")

        # Pencil Sketch conversion logic
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted = 255 - gray_image
        blur = cv2.GaussianBlur(inverted, (21, 21), 0)
        invertedblur = 255 - blur
        sketch = cv2.divide(gray_image, invertedblur, scale=256.0)

        # Save the result
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(str(output_path), sketch)
        return True

