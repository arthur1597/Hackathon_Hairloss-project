import torch
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models.segmentation as segmentation
from sklearn.metrics import precision_score
import os

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.unet = segmentation.fcn_resnet50(pretrained=False)

    def forward(self, x):
        return self.unet(x)['out']

class YOLO_UNet:
    def __init__(self, yolo_model_path, unet_model_path):
        self.yolo_model = YOLO(yolo_model_path)
        self.yolo_model.to(device)
        self.yolo_model.eval()

        self.unet_model = UNet().to(device)
        unet_state_dict = torch.load(unet_model_path, map_location=device)
        self.unet_model.unet.load_state_dict(unet_state_dict, strict=False)
        self.unet_model.eval()

    def detect_and_segment(self, input_image):
        image_path = input_image.filename
        detections = self.yolo_model.predict(source=image_path, imgsz=640, conf=0.5)
        results = []

        for detection in detections[0].boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0].tolist())
            bbox = (x1, y1, x2, y2)

            cropped_image = input_image.crop(bbox)

            input_tensor = self.prepare_unet_input(cropped_image)

            with torch.no_grad():
                input_tensor = input_tensor.to(device)
                mask = self.unet_model(input_tensor)
                mask = torch.sigmoid(mask).cpu().squeeze().numpy()

            results.append({'bbox': bbox, 'mask': mask})

        return results

    def prepare_unet_input(self, cropped_image):
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])
        input_tensor = transform(cropped_image).unsqueeze(0)
        return input_tensor

    def show_results(self, input_image, results):
        detection_image = input_image.copy()
        draw = ImageDraw.Draw(detection_image)
        for result in results:
            bbox = result['bbox']
            x1, y1, x2, y2 = bbox
            draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
        plt.figure(figsize=(10, 10))
        plt.imshow(detection_image)
        plt.title('Detection Results')
        plt.axis('off')
        plt.show()

        
        for idx, result in enumerate(results):
            mask = result['mask'][0] 
            bbox = result['bbox']
            mask_resized = Image.fromarray((mask * 255).astype(np.uint8)).resize((bbox[2] - bbox[0], bbox[3] - bbox[1]))
            mask_image = Image.new('L', input_image.size, 0)
            mask_image.paste(mask_resized, (bbox[0], bbox[1]))
            plt.figure(figsize=(10, 10))
            plt.imshow(mask_image, cmap='gray')
            plt.title(f'Mask Result {idx}')
            plt.axis('off')
            plt.show()

def generate_masks(damage_dir, origin_dir, mask_dir):
    damage_files = sorted(os.listdir(damage_dir))
    origin_files = sorted(os.listdir(origin_dir))

    for damage_file, origin_file in zip(damage_files, origin_files):
        damage_img_path = os.path.join(damage_dir, damage_file)
        origin_img_path = os.path.join(origin_dir, origin_file)
        mask_img_path = os.path.join(mask_dir, damage_file)


        damage_img = Image.open(damage_img_path).convert("L") 
        origin_img = Image.open(origin_img_path).convert("L")  

        damage_array = np.array(damage_img, dtype=np.uint8)
        origin_array = np.array(origin_img, dtype=np.uint8)

        mask_array = np.where(damage_array != origin_array, 1, 0).astype(np.uint8)


        mask_img = Image.fromarray(mask_array * 255)  
        mask_img.save(mask_img_path)

if __name__ == "__main__":
    yolo_model_path = "/kaggle/input/yolobest/pytorch/default/1/Only_YOLO.pt"
    unet_model_path = "/kaggle/input/yolounet/pytorch/default/1/unet_model.pth"

    model = YOLO_UNet(yolo_model_path, unet_model_path)
    input_image = Image.open("/kaggle/input/qwerqwt/KakaoTalk_20241201_110239190.jpg")

    results = model.detect_and_segment(input_image)
    predicted_masks = []

    for result in results:
        bbox = result['bbox']
        mask = result['mask']
        predicted_masks.append(mask)

        print("Bounding Box:", bbox)

    # Show the results
    model.show_results(input_image, results)
  
