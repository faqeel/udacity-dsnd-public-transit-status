![Final User Interface](images/ui.png)

# Public Transit Status with Apache Kafka

This project demonstrates a real-time streaming pipeline for public transit data from the [Chicago Transit Authority](https://www.transitchicago.com/data/). It leverages the Apache Kafka ecosystem, including tools like Kafka Connect and the Confluent REST Proxy, to simulate and display the real-time status of train lines. This project was developed as part of Udacity's Data Streaming Nanodegree.


## Architecture

![Project Architecture](images/diagram.png)

## Getting Started

To run this project, you will need Docker and Docker Compose installed on your machine.

Start all the necessary services, including Kafka brokers, Zookeeper, and various Confluent Platform tools, using Docker Compose.

```sh
docker-compose up
```

Once the services are running, you can access the following services:

| Service | Host URL | Docker URL | Username | Password |
| --- | --- | --- | --- | --- |
| Public Transit Status | [http://localhost:8888](http://localhost:8888) | n/a | ||
| Landoop Kafka Connect UI | [http://localhost:8084](http://localhost:8084) | http://connect-ui:8084 |
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085) | http://topics-ui:8085 |
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086) | http://schema-registry-ui:8086 |
| Kafka | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094 | PLAINTEXT://kafka0:9092,PLAINTEXT://kafka1:9093,PLAINTEXT://kafka2:9094 |
| REST Proxy | [http://localhost:8082](http://localhost:8082/) | http://rest-proxy:8082/ |
| Schema Registry | [http://localhost:8081](http://localhost:8081/ ) | http://schema-registry:8081/ |
| Kafka Connect | [http://localhost:8083](http://localhost:8083) | http://kafka-connect:8083 |
| KSQL | [http://localhost:8088](http://localhost:8088) | http://ksql:8088 |
| PostgreSQL | `jdbc:postgresql://localhost:5432/cta` | `jdbc:postgresql://postgres:5432/cta` | `cta_admin` | `chicago` |

### Run the Data Pipeline

The pipeline consists of three main components that need to be run in a specific order: a data producer, a Faust stream processing application, and a KSQL script.

First, set up the Python environment for both producers and consumers:

```sh
# Create and activate a virtual environment
virtualenv venv
source venv/bin/activate

# Install required packages
pip install -r producers/requirements.txt
pip install -r consumers/requirements.txt
```

#### Step A: Start the Producer

This script simulates the CTA train events and publishes them to Kafka topics.

```sh
python producers/simulation.py
```

#### Step B: Start the Faust Stream Processing Application

This application consumes the data, processes it, and prepares it for display.

```sh
python consumers/faust_stream.py worker -l info
```

#### Step C: Create KSQL Table:

This script uses KSQL to define a streaming table that will be used by the pipeline.

```sh
python consumers/ksql.py
```

### View the Real-time Dashboard

Finally, start the web server to see the real-time dashboard.

```sh
python consumers/server.py
```

The application will be available at [http://localhost:8888](http://localhost:8888). You can now see the train line statuses updating in real time.

To stop all services and clean up, run:

```sh
docker-compose down
```
