import cv2
import os
from pathlib import Path

class ImageToArtService:
    @staticmethod
    def process(input_path: str | Path, output_path: str | Path, mode: str = "sketch"):
        """
        Processes an image into various artistic styles.
        """
        image = cv2.imread(str(input_path))
        if image is None:
            raise FileNotFoundError(f"Could not load image from {input_path}")

        if mode == "oil":
            # Stylized / Oil Paint-like effect using stylization filter
            # Parameters: sigma_s=60, sigma_r=0.4 are good defaults
            result = cv2.stylization(image, sigma_s=60, sigma_r=0.45)
        else:
            # Default: Pencil Sketch conversion
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            inverted = 255 - gray_image
            blur = cv2.GaussianBlur(inverted, (21, 21), 0)
            invertedblur = 255 - blur
            result = cv2.divide(gray_image, invertedblur, scale=256.0)

        # Save the result
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(str(output_path), result)
        return True

