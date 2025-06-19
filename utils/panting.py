import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
from PIL import Image
import os
import time
import gc


MODEL_PATH = "models/panting.pth" 
IMG_SIZE = 224
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
FRAME_INTERVAL = 1
THRESHOLD = 0.5
