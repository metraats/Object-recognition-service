FROM python:3.12

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY . /app/
COPY data /app/data/
COPY proto /app/proto/
COPY tests /app/tests/

EXPOSE 8080 9090

CMD sh -c "python3 /app/inference-api.py & cd /app/proto && python3 client-api.py"