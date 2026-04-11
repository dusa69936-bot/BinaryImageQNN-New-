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

        print(f"[OK] CNN Model Loaded Successfully from: {MODEL_PATH}")

    else:
        print(f"[ERROR] Model file not found: {MODEL_PATH}")

except Exception as e:
    print(f"[ERROR] Error loading model: {e}")


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

# =============================
# PREDICT WITH ATTENTION MAP
# =============================

def predict_digit_with_attention(image):
    try:
        # Preprocess
        img_np = preprocess_image(image)
        
        # ⚠️ Force gradient tracking for Saliency/Grad-CAM
        img_tensor = torch.tensor(img_np.tolist(), requires_grad=True).float()

        # Forward pass
        output = model(img_tensor)
        probs = torch.exp(output)
        confidence, predicted = torch.max(probs, 1)
        pred_idx = predicted.item()

        # Backward pass
        score = output[0, pred_idx]
        model.zero_grad()
        score.backward()

        # 1. Grad-CAM style Heatmap (Gradients)
        grads = img_tensor.grad.data.abs().reshape(28, 28).numpy()
        grads = (grads - grads.min()) / (grads.max() - grads.min() + 1e-8)
        
        # 2. Attention Map (Pixel intensity + partial gradients)
        raw_pixels = img_np.reshape(28, 28)
        attention = (raw_pixels * 0.7 + grads * 0.3)
        attention = (attention - attention.min()) / (attention.max() - attention.min() + 1e-8)

        from PIL import Image as PILImage
        import base64
        import io

        def to_b64(arr, color_tint=None):
            arr_uint8 = (arr * 255).astype(np.uint8)
            img = PILImage.fromarray(arr_uint8, mode='L').resize((280, 280), PILImage.LANCZOS)
            
            if color_tint == 'heatmap':
                # Pseudo-color: Red for high, Blue for low
                from PIL import ImageOps
                colored = PILImage.new("RGB", (280, 280))
                # Simple Red-Yellow-Blue tint
                for x in range(280):
                    for y in range(280):
                        v = img.getpixel((x,y))
                        if v > 150: colored.putpixel((x,y), (v, 50, 50)) # Red
                        elif v > 50: colored.putpixel((x,y), (v, v, 0)) # Yellow
                        else: colored.putpixel((x,y), (0, 0, v)) # Blue
                img = colored
            elif color_tint == 'attention':
                # Pink tint
                colored = PILImage.new("RGB", (280, 280))
                for x in range(280):
                    for y in range(280):
                        v = img.getpixel((x,y))
                        colored.putpixel((x,y), (v, v//4, v//2)) # Pink
                img = colored

            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

        heatmap_b64 = to_b64(grads, 'heatmap')
        attention_b64 = to_b64(attention, 'attention')

        return int(pred_idx), round(float(confidence.item()) * 100, 2), heatmap_b64, attention_b64

    except Exception as e:
        import traceback
        print("[ERROR] Attention Prediction Error:", traceback.format_exc())
        p, c = predict_digit(image)
        return p, c, "", ""

def predict_digit(image):
    try:
        img = preprocess_image(image)
        try:
            img = torch.tensor(img)
        except Exception:
            img = torch.tensor(img.tolist())
            
        img = img.float()

        with torch.no_grad():
            output = model(img)
            probs = torch.exp(output)
            confidence, predicted = torch.max(probs, 1)

        return int(predicted.item()), round(float(confidence.item()) * 100, 2)

    except Exception as e:
        import traceback
        print("[ERROR] Prediction Error:", traceback.format_exc())
        return -1, str(e)