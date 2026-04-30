import json
import time
import random
from confluent_kafka import Producer
from datetime import datetime

# Configuração do Kafka
producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'telemetria-bruta'
vehicle_id = 'CAMINHAO-001'

print(f"Iniciando sensor do {vehicle_id}...")

while True:
    # Simula a leitura do sensor
    speed = random.uniform(60.0, 100.0) 
    event = {
        'vehicle_id': vehicle_id,
        'speed': round(speed, 2),
        'timestamp': datetime.now().isoformat()
    }
    
    # Publica o evento no Kafka
    producer.produce(topic, key=vehicle_id, value=json.dumps(event).encode('utf-8'))
    producer.flush()
    
    print(f"[Sensor] Enviado: {event}")
    time.sleep(2) # Envia a cada 2 segundos