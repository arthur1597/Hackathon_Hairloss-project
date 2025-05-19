import warnings
warnings.filterwarnings('ignore')

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import yaml
import torch
from PIL import Image
from ultralytics import YOLO
from IPython.display import Video

sns.set(rc={'axes.facecolor': '#eae8fa'}, style='darkgrid')

model = YOLO("yolo11n.pt")

image_path = '/kaggle/input/qweqras/test/images/1.rf.fec1fea0a9eee511582d1635b943feb2.jpg'
results = model.predict(source=image_path,
                        imgsz=640,
                        verbose=False,
                        conf=0.5)  


sample_image = results[0].plot(line_width=2)

sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(20,15))
plt.imshow(sample_image)
plt.title('Pre_trained Yolov11 Model', fontsize=20)
plt.axis('off')
plt.show()
