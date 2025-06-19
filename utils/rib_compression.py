import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
from PIL import Image
import os
import time
import gc

# --- CONFIG ---
MODEL_PATH = "models/rib_compression.pth"
IMG_SIZE = 224
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
FRAME_INTERVAL = 1
THRESHOLD = 0.5

# --- Load Model ---
def load_rib_model():
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, 1)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

# --- Transform ---
rib_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

# --- Predict Frame Confidence & Label ---
def predict_rib_frame(model, frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = rib_transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = torch.sigmoid(model(image)).item()
    return output, 1 if output > THRESHOLD else 0

