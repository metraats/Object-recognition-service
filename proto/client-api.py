import grpc
from concurrent import futures
import tests.inference_pb2 as inference_pb2
import tests.inference_pb2_grpc as inference_pb2_grpc
import requests
import torch
import io
import json
from PIL import Image
from torchvision import models, transforms

# Загружаем модель
model = models.detection.maskrcnn_resnet50_fpn(weights=models.detection.MaskRCNN_ResNet50_FPN_Weights.COCO_V1)
model.eval()

# Загружаем категории COCO
with open("../ data/coco_categories.json", "r") as f:
    COCO_CATEGORIES = json.load(f)

# Трансформация изображения
transform = transforms.Compose([
    transforms.ToTensor(),
])


class InstanceDetectorServicer(inference_pb2_grpc.InstanceDetectorServicer):
    def Predict(self, request, context):
        image_url = request.url

        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Error loading image: {str(e)}")
            return inference_pb2.InstanceDetectorOutput(objects=[])

        image_tensor = transform(image)
        with torch.no_grad():
            predictions = model([image_tensor])

        detected_objects = [
            COCO_CATEGORIES[label - 1] for label, score in
            zip(predictions[0]['labels'].tolist(), predictions[0]['scores'].tolist())
            if score >= 0.75
        ]

        return inference_pb2.InstanceDetectorOutput(objects=detected_objects)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InstanceDetectorServicer_to_server(InstanceDetectorServicer(), server)
    server.add_insecure_port('[::]:9090')
    server.start()
    print("gRPC server started on port 9090")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
