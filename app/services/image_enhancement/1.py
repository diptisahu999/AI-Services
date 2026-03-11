import cv2
import numpy as np
import os
# import torch
# from basicsr.utils import imwrite
# import warnings
import sys
# sys.path.append("./ImgEnhancement")
from gfpgan import GFPGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

class ImgDeblur:
    def __init__(self, bg_upsampler=True):
        if bg_upsampler:
            bg_tile = 400
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            model_url = r'F:\Ranjan\Demo-Project-Personal\ai_service_fastapi\app\services\image_enhancement\RealESRGAN_x2plus.pth'
            if not os.path.exists(model_url):
                raise FileNotFoundError(f"RealESRGAN model file not found: {model_url}")
            self.bg_upsampler = RealESRGANer(
                scale=2,
                model_path=model_url,
                model=model,
                tile=bg_tile,
                tile_pad=10,
                pre_pad=0,
                half=False  
            )
        else:
            self.bg_upsampler = None

        arch = 'clean'
        channel_multiplier = 2
        gfp_model_path = r'F:\Ranjan\Demo-Project-Personal\ai_service_fastapi\app\services\image_enhancement\GFPGANv1.3.pth'
        
        if not os.path.exists(gfp_model_path):
            raise FileNotFoundError(f"GFPGAN model file not found: {gfp_model_path}")
        
        self.restorer = GFPGANer(
            model_path=gfp_model_path,
            upscale=2,
            arch=arch,
            channel_multiplier=channel_multiplier,
            bg_upsampler=self.bg_upsampler
        )
    def process_image(self, img_path, output_image_path):
        input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if input_img is None:
            raise ValueError(f"Image not found or cannot be read: {img_path}")
        
        h, w = input_img.shape[:2]

        cropped_faces, restored_faces, restored_img = self.restorer.enhance(
            input_img,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=0.5
        )

        if not isinstance(restored_img, np.ndarray):
            raise TypeError(f"Expected numpy.ndarray for restored_img, but got {type(restored_img)}")

        # Resize back to original size to maintain input-output dimensions
        restored_img = cv2.resize(restored_img, (w, h), interpolation=cv2.INTER_LANCZOS4)

        if not cv2.imwrite(output_image_path, restored_img):
            raise IOError(f"Failed to write image to {output_image_path}")
        print(f"Processed image saved to: {output_image_path}")


if __name__ == "__main__":
    input_directory = r'E:\TechVizor\AI Service App\ai_service_fastapi\app\services\image_enhancement\data'
    output_directory = r'E:\TechVizor\AI Service App\ai_service_fastapi\app\services\image_enhancement\ImgEnhancement'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        img_deblur = ImgDeblur()
        print("ImgDeblur instance created successfully.")
        
        for filename in os.listdir(input_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                input_image_path = os.path.join(input_directory, filename)
                output_image_path = os.path.join(output_directory, filename)
                img_deblur.process_image(input_image_path, output_image_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")







# github =  https://github.com/TencentARC/GFPGAN?tab=readme-ov-file