import torch
from torch import nn
import numpy as np
import os
from PIL import Image

# =============================
# CNN MODEL (MATCHES YOUR model.pth)
# =============================

class CNN(nn.Module):

    def __init__(self):
        super().__init__()

        # ✅ FIX: change 16 → 32
        self.conv = nn.Conv2d(1, 32, 3)

        self.pool = nn.MaxPool2d(2, 2)

        # ⚠️ FC size stays same (based on your error log)
        self.fc = nn.Linear(5408, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv(x)))
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return torch.log_softmax(x, dim=1)


# =============================
# MODEL PATH
# =============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    os.path.dirname(BASE_DIR),
    "mnist-canvas",
    "mnist",
    "model.pth"
)

# =============================
# LOAD MODEL
# =============================

model = CNN()

try:
    if os.path.exists(MODEL_PATH):

        model.load_state_dict(
            torch.load(MODEL_PATH, map_location=torch.device("cpu"))
        )

        model.eval()

        print(f"✅ CNN Model Loaded Successfully from: {MODEL_PATH}")

    else:
        print(f"❌ Model file not found: {MODEL_PATH}")

except Exception as e:
    print(f"❌ Error loading model: {e}")


# =============================
# IMAGE PREPROCESS FUNCTION
# =============================

def preprocess_image(image):
    from PIL import ImageOps
    import numpy as np

    # convert to grayscale
    image = image.convert("L")

    # 🔥 Auto-invert if the user drew black ink on a white board 
    # (Because the model's bounding box and tensors expect white ink on black padding)
    if np.mean(np.array(image)) > 127:
        image = ImageOps.invert(image)

    # Tightly crop the non-zero (white) bounding box
    bbox = image.getbbox()
    if bbox:
        # crop to the digit
        image = image.crop(bbox)
        
        # make it a square by padding the shorter side
        w, h = image.size
        max_dim = max(w, h)
        
        # center the digit in the square box
        sq_img = Image.new("L", (max_dim, max_dim), 0)
        sq_img.paste(image, ((max_dim - w) // 2, (max_dim - h) // 2))
        
        # Add 20% border padding (like MNIST)
        pad = int(max_dim * 0.25)
        final_dim = max_dim + pad * 2
        
        padded_img = Image.new("L", (final_dim, final_dim), 0)
        padded_img.paste(sq_img, (pad, pad))
        image = padded_img

    # resize to MNIST size using high-quality resampling
    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
    image = image.resize((28, 28), resample_filter)

    # convert to numpy
    img = np.array(image, dtype=np.float32)

    # normalize
    img = img / 255.0

    # reshape → (1,1,28,28)
    img = img.reshape(1, 1, 28, 28)

    return img


# =============================
# PREDICT FUNCTION
# =============================

def predict_digit(image):

    try:

        img = preprocess_image(image)

        img = torch.tensor(img).float()

        with torch.no_grad():
            output = model(img)
            probs = torch.exp(output)
            confidence, predicted = torch.max(probs, 1)

        return int(predicted.item()), round(float(confidence.item()) * 100, 2)

    except Exception as e:

        import traceback
        print("❌ Prediction Error:", traceback.format_exc())
        return -1, str(e)