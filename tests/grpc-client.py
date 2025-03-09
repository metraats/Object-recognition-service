import grpc
import inference_pb2
import inference_pb2_grpc

channel = grpc.insecure_channel("localhost:9090")
stub = inference_pb2_grpc.InstanceDetectorStub(channel)

response = stub.Predict(inference_pb2.InstanceDetectorInput(
    url="http://images.cocodataset.org/val2017/000000001268.jpg"
))

print(response.objects)
