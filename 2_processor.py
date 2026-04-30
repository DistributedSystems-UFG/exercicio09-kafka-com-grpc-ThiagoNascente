import json
from confluent_kafka import Consumer, Producer

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-processamento',
    'auto.offset.reset': 'latest'
})
producer = Producer({'bootstrap.servers': 'localhost:9092'})

topic_in = 'telemetria-bruta'
topic_out = 'eventos-frota'
consumer.subscribe([topic_in])

print("Iniciando processador de stream...")

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue
    if msg.error(): continue

    data = json.loads(msg.value().decode('utf-8'))
    
    # Regra de negócio: Identificar excesso de velocidade
    status = "ALERTA_EXCESSO_VELOCIDADE" if data['speed'] > 80.0 else "NORMAL"
    
    processed_event = {
        'vehicle_id': data['vehicle_id'],
        'average_speed': data['speed'], # Em um cenário real, faríamos a média aqui
        'status': status,
        'timestamp': data['timestamp']
    }

    # Publica a nova informação
    producer.produce(topic_out, key=data['vehicle_id'], value=json.dumps(processed_event).encode('utf-8'))
    producer.flush()
    
    print(f"[Processador] Processado e encaminhado: {processed_event}")