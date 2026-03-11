import os
import cv2
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from diffusers.utils import load_image

# Initialize the image cartoonization pipeline
img_cartoon = pipeline(Tasks.image_portrait_stylization, 
                       model='damo/cv_unet_person-image-cartoon_compound-models')

# Define the source and target directories
base_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(base_dir, "color_image")
target_dir = os.path.join(base_dir, "anime_image")

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Process each image in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
        img_path = os.path.join(source_dir, filename)
        print(f'Processing {img_path}')

        # Process the image
        result = img_cartoon(img_path)
        result_img = result[OutputKeys.OUTPUT_IMG]

        # Save the processed image
        target_path = os.path.join(target_dir, filename)
        cv2.imwrite(target_path, result_img)
        print(f'Saved processed image to {target_path}')
