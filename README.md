# Object-recognition-service

Билд докера:
```
docker build -t object-detection-service .    
```

Запускаем полученный докер:
```
docker run -p 8080:8080 -p 9090:9090 object-detection-service
```

Дальше можно посылать запросы с ссылкой на фотографию на порт 8080 или 9090 и получать список объектов на фотографии, пример:
```
curl -XPOST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"url": "http://images.cocodataset.org/val2017/000000001268.jpg"}' 
...
{
  "objects": [
        "bird",
        "boat",
        "boat",
        "person",
        "person",
        "person",
        "person",
        "cell phone",
        "backpack",
        "handbag",
        "boat"
    ]
}
```

Также можно смотреть метрики приложения, в частности-число вызовов ручки /predict:
```
curl http://localhost:8080/metrics
...
# HELP app_http_inference_count_total Multiprocess metric
# TYPE app_http_inference_count_total counter
app_http_inference_count_total 12.0
```

Есть папка с тестами tests с соответсвующими тестами в файле test.py и gt разметкой в файлах eval.json и eval_big.json. Тесты запускаются с нужным окружением (requirements.txt) командой:
```
python -m pytest tests.py
```