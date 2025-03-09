FROM python:3.12

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY . /app/
COPY data/ /app/data/
COPY proto/ /app/proto/

EXPOSE 8080 9090

CMD sh -c "python3 /app/client-api.py & python3 /app/inference-api.py"

####

WORKDIR /app

# Копируем все файлы API
COPY client-api.py inference-api.py inference_pb2.py inference_pb2_grpc.py /app/
COPY data/coco_categories.json /app/data/

# Открываем порты для HTTP (8080) и gRPC (9090)
EXPOSE 8080 9090

# Запускаем gRPC API в фоне, затем HTTP API
CMD sh -c "python3 /app/client-api.py & python3 /app/inference-api.py"