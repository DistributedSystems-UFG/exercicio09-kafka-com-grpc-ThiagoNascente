[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/A6uVSc3Y)

somente pela máquina da aws (quatro máquinas - <tipo>)

## Requisitos

- 5 máquinas t3-small (aws)
- Todas compartilhando a pasta /mnt/efs/fs1
- Portas 9092, 50051

### Maquina 1

```bash
cd /mnt/efs/fs1
```

```bash
sudo apt update
```

```bash
sudo apt install default-jdk
```

```bash
wget https://dlcdn.apache.org/kafka/4.2.0/kafka_2.13-4.2.0.tgz
```

```bash
tar -xzf kafka_2.13-4.2.0.tgz
```

```bash
cd kafka_2.13-4.2.0/
```

```bash
nano config/server.properties
```

```bash
advertised.listeners=PLAINTEXT://<IP_PUBLICO_MAQUINA_1>:9092,CONTROLLER://localhost:9093
```

- CTRL + O
- ENTER
- CTRL + X

```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
```

```bash
bin/kafka-server-start.sh config/server.properties
```

```bash
bin/kafka-topics.sh --create --topic telemetria-bruta --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic eventos-frota --bootstrap-server localhost:9092
```

### Maquina 2

- Cria e ativa o ambiente virtual

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

- Instala as dependências

```bash
pip3 install confluent-kafka grpcio grpcio-tools
```

- Compilar

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/fleet.proto
```

```bash
python 3_server.py
```

### Maquina 3

```bash
python 2_processor.py
```

### Maquina 4

```bash
python 1_sensor.py
```

### Maquina 5

```bash
python 4_client.py
```


