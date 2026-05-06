[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/A6uVSc3Y)

somente pela máquina da aws (quatro máquinas - <tipo>)

## Requisitos

- 5 máquinas t3-small (aws)
- Todas compartilhando a pasta /mnt/efs/fs1

### Maquina 1

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

### Maquina 3

### Maquina 4

### Maquina 5

# Kafka

> Fluxo para ajeitar o kafka

# Grpc

> Fluxo para ajeitar o Grpc


