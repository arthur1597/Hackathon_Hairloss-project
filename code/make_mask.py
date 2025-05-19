import os
import numpy as np
from PIL import Image
import pandas as pd
import cv2


mask_dir = '/kaggle/working/train_mask2'
os.makedirs(mask_dir, exist_ok=True)

def generate_masks_with_bboxes(image_dir, bbox_dir, mask_dir):
    image_files = sorted(os.listdir(image_dir))
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        bbox_path = os.path.join(bbox_dir, os.path.splitext(image_file)[0] + ".txt")
        mask_path = os.path.join(mask_dir, image_file)

        image = Image.open(image_path).convert("L")  # 흑백 이미지로 변환
        image_array = np.array(image)
        height, width = image_array.shape


        mask = np.zeros((height, width), dtype=np.uint8)


        if not os.path.exists(bbox_path):
            print(f"바운딩 박스 파일이 없습니다: {bbox_path}")
            continue

        bboxes = pd.read_csv(bbox_path, delim_whitespace=True, header=None)
        bboxes.columns = ["class", "x_center", "y_center", "bbox_width", "bbox_height"]


        for _, row in bboxes.iterrows():
            x_center = float(row['x_center']) * width
            y_center = float(row['y_center']) * height
            bbox_width = float(row['bbox_width']) * width
            bbox_height = float(row['bbox_height']) * height

            x_min = int(x_center - bbox_width / 2)
            y_min = int(y_center - bbox_height / 2)
            x_max = int(x_center + bbox_width / 2)
            y_max = int(y_center + bbox_height / 2)

    
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(width, x_max)
            y_max = min(height, y_max)


            bbox_region = image_array[y_min:y_max, x_min:x_max]
용
            equalized_region = cv2.equalizeHist(bbox_region)


            blurred_region = cv2.GaussianBlur(equalized_region, (5, 5), 0)

            adaptive_mask = cv2.adaptiveThreshold(
                blurred_region,
                maxValue=255,
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv2.THRESH_BINARY_INV,
                blockSize=11,
                C=2
            )

            mask[y_min:y_max, x_min:x_max] = adaptive_mask

        mask_img = Image.fromarray(mask)
        mask_img.save(mask_path)
        print(f"마스크 저장 완료: {mask_path}")


generate_masks_with_bboxes(
    image_dir='/kaggle/input/qweqras/train/images',  
    bbox_dir='/kaggle/input/qweqras/train/labels',  
    mask_dir=mask_dir  
)
print(f" 마스크 생성 및 저장 완료: {mask_dir}")
