import grpc
import proto.fleet_pb2 as fleet_pb2
import proto.fleet_pb2_grpc as fleet_pb2_grpc
import time

def run():
    print("Iniciando cliente gRPC do Gestor de Frota...")
    # Conecta ao servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = fleet_pb2_grpc.FleetServiceStub(channel)
        
        vehicle_id = "CAMINHAO-001"
        
        # Faz consultas periódicas simulando o usuário atualizando o painel
        for _ in range(5):
            print(f"\n[Cliente] Consultando status de {vehicle_id}...")
            try:
                request = fleet_pb2.VehicleRequest(vehicle_id=vehicle_id)
                response = stub.GetVehicleStatus(request)
                print(f" > Velocidade Atual: {response.average_speed} km/h")
                print(f" > Status: {response.status}")
                print(f" > Última atualização: {response.last_updated}")
            except grpc.RpcError as e:
                print(f"Erro gRPC: {e.details()} (Código: {e.code()})")
            
            time.sleep(3)

if __name__ == '__main__':
    run()