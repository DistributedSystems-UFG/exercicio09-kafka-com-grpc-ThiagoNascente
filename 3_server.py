import grpc
import json
import sqlite3
import threading
from concurrent import futures
from confluent_kafka import Consumer

import proto.fleet_pb2 as fleet_pb2
import proto.fleet_pb2_grpc as fleet_pb2_grpc

# 1. Configuração do Banco de Dados (SQLite)
def setup_db():
    conn = sqlite3.connect('fleet.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicle_state (
            vehicle_id TEXT PRIMARY KEY,
            average_speed REAL,
            status TEXT,
            last_updated TEXT
        )
    ''')
    conn.commit()
    return conn

db_conn = setup_db()

# 2. Worker do Kafka (Consome eventos e salva no DB)
def kafka_consumer_worker():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'grupo-webservice',
        'auto.offset.reset': 'latest'
    })
    consumer.subscribe(['eventos-frota'])
    
    print("[Kafka Worker] Escutando eventos processados...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error(): continue
        
        data = json.loads(msg.value().decode('utf-8'))
        
        # Upsert no SQLite
        cursor = db_conn.cursor()
        cursor.execute('''
            INSERT INTO vehicle_state (vehicle_id, average_speed, status, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(vehicle_id) DO UPDATE SET
                average_speed=excluded.average_speed,
                status=excluded.status,
                last_updated=excluded.last_updated
        ''', (data['vehicle_id'], data['average_speed'], data['status'], data['timestamp']))
        db_conn.commit()
        print(f"[DB Write] Estado atualizado para {data['vehicle_id']}")

# 3. Implementação do Servidor gRPC
class FleetServiceServicer(fleet_pb2_grpc.FleetServiceServicer):
    def GetVehicleStatus(self, request, context):
        cursor = db_conn.cursor()
        cursor.execute('SELECT average_speed, status, last_updated FROM vehicle_state WHERE vehicle_id = ?', (request.vehicle_id,))
        row = cursor.fetchone()
        
        if row:
            return fleet_pb2.VehicleResponse(
                vehicle_id=request.vehicle_id,
                average_speed=row[0],
                status=row[1],
                last_updated=row[2]
            )
        else:
            # Retorna um erro gRPC caso o veículo não exista
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Veículo não encontrado.')
            return fleet_pb2.VehicleResponse()

# 4. Inicialização
if __name__ == '__main__':
    # Inicia o worker do Kafka em background
    threading.Thread(target=kafka_consumer_worker, daemon=True).start()
    
    # Inicia o servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fleet_pb2_grpc.add_FleetServiceServicer_to_server(FleetServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("[gRPC Server] Rodando na porta 50051...")
    server.wait_for_termination()