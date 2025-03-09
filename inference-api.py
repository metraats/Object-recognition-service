import io
import requests
import json
import torch

from PIL import Image
from flask import Flask, request, jsonify
from torchvision import models, transforms
from prometheus_client import Counter
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)

metrics = PrometheusMetrics(app)

# Модель
model = models.detection.maskrcnn_resnet50_fpn(weights=models.detection.MaskRCNN_ResNet50_FPN_Weights.COCO_V1)
model.eval()

# Метки
LABELS_PATH = "data/coco_categories.json"
with open(LABELS_PATH, "r") as f:
    COCO_CATEGORIES = json.load(f)

# Трансформации
transform = transforms.Compose([
    transforms.ToTensor(),
])


@app.route('/predict', methods=['POST'])
@metrics.counter("app_http_inference_count_total", "Number of HTTP inference requests")
def predict():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400
        
    try:
        response = requests.get(data["url"])
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Error loading image: {str(e)}"}), 400
    
    image_tensor = transform(image)
    with torch.no_grad():
        predictions = model([image_tensor])

    detected_objects = [COCO_CATEGORIES[label-1] for label, score in 
                        zip(predictions[0]['labels'].tolist(), predictions[0]['scores'].tolist()) 
                        if score >= 0.75]
    
    return jsonify({"objects": detected_objects})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
