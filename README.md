# Real-Time Data Pipeline with Apache Spark, Kafka, Cassandra, and Yahoo Finance

This project sets up a real-time data pipeline that captures financial data from Yahoo Finance via WebSocket, processes it using Apache Spark Structured Streaming, and stores the results in Apache Cassandra. It utilizes Docker for containerization and orchestration.

![Diagramme sans nom drawio](https://github.com/Ayoub-Talbi1/Real-Time-Financial-Data-Pipeline/assets/86127094/4f300f3a-690f-4ccc-a1c9-7adc53054fce)


## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Overview](#project-overview)
- [Building Docker Images](#building-docker-images)
- [Docker Compose Setup](#docker-compose-setup)
- [Setting Up Cassandra](#setting-up-cassandra)
- [Setting Up Kafka](#setting-up-kafka)
- [Setting Up Spark Master](#setting-up-spark-master)
- [Running the Data Pipeline](#running-the-data-pipeline)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before getting started, make sure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Overview

This project sets up a data pipeline to capture real-time financial data from Yahoo Finance using WebSocket. It then processes this data using Apache Spark Structured Streaming and stores the results in Apache Cassandra. Here's an overview of the key components:

- **Yahoo Finance WebSocket**: We use the `yliveticker` library to connect to Yahoo Finance WebSocket and fetch financial data for specified tickers.

- **Kafka**: Apache Kafka is used as a message broker to transport data from the WebSocket to the Spark application.

- **Spark Structured Streaming**: Apache Spark is used to process the streaming data. We create a Spark job that consumes data from Kafka, performs data transformation and aggregation, and then stores it in Cassandra.

- **Cassandra**: Apache Cassandra is used to store the processed financial data. We create a keyspace and table in Cassandra to accommodate the data.

## Building Docker Images

Before setting up the Docker Compose environment, you need to build the Docker images. We provide a Dockerfile for Apache Spark. Follow these steps to build the images:

1. Clone this repository.

2. Navigate to the project directory.

3. Run the following command to build the Docker image:

   ```bash
   docker build -t cluster-apache-spark:3.0.2 .
   ```

   This command builds the Apache Spark image used in the Spark cluster setup.

## Docker Compose Setup

The project is containerized using Docker Compose. To set up the environment, follow these steps:

1. Clone this repository.

2. Navigate to the project directory.

3. Run the following command to start the containers:

   ```bash
   docker-compose up -d
   ```

   This will start the Spark Master, Spark Workers, Cassandra, Kafka, and Zookeeper containers.

4. To check if the containers are running, you can use:

   ```bash
   docker-compose ps
   ```

   You should see all containers in an "Up" state.

## Setting Up Cassandra

1. Access the Cassandra container:

   ```bash
   docker exec -it cassandra-container bash
   ```

2. Start the Cassandra shell:

   ```bash
   cqlsh
   ```

3. Create a keyspace and table:

   ```sql
   CREATE KEYSPACE streams WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
   use streams;
   CREATE TABLE yahoofinance (
       id UUID PRIMARY KEY,
       exchange TEXT,
       quoteType DOUBLE,
       price DOUBLE,
       timestamp DOUBLE,
       marketHours DOUBLE,
       changePercent DOUBLE,
       dayVolume DOUBLE,
       change DOUBLE,
       priceHint DOUBLE,
       cumulative_avg_price DOUBLE
   );
   ```

4. Verify the table creation:

   ```sql
   SELECT COUNT(*) FROM yahoofinance;
   ```

   This should return `0`, as no data has been inserted yet.

## Setting Up Kafka

1. Access the Kafka container:

   ```bash
   docker exec -it -u root kafka-container bash
   ```

2. Install necessary packages:

   ```bash
   yum install nano python3 python3-pip
   ```

3. Install Python dependencies:

   ```bash
   pip3 install yliveticker pykafka
   ```

4. copy the Python script named `producer.py` to the kafka-container:

   ```bash
   docker cp scripts/producer.py kafka-container:/producer.py
   ```

   This script fetches financial data from Yahoo Finance WebSocket and sends it to Kafka.

## Setting Up Spark Master

1. Access the Spark Master container:

   ```bash
   docker exec -it -u root spark-master bash
   ```

2. Install necessary packages:

   ```bash
   apt-get install nano python3 python3-pip
   ```

3. Install PySpark:

   ```bash
   pip3 install pyspark
   ```

4. Copy the Python script named `consumer.py` to the spark master container:

   ```python
   docker cp scripts/consumer.py (spark-master-container-id):/opt/spark/consumer.py
   ```

   This script consumes data from Kafka, processes it using Spark Structured Streaming, and stores it in Cassandra.

## Running the Data Pipeline

With all the containers set up and the scripts in place, the data pipeline is ready to run. Follow these steps to start the pipeline:

1. Start the Kafka producer script (inside the Kafka container):

   ```bash
   python3 producer.py
   ```

   This script fetches financial data from Yahoo Finance WebSocket and sends it to Kafka.

2. Start the Spark job (inside the Spark Master container):

   ```bash
   /opt/spark/bin/spark-submit --master spark://spark-master:7077 --jars /opt/spark-apps/postgresql-42.2.22.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2 --driver-memory 1G --executor-memory 1G /opt/spark/consumer.py
   ```

   This job consumes data from Kafka, processes it using Spark Structured Streaming, and stores it in Cassandra.

The pipeline is now running, capturing real-time financial data and storing it in Cassandra.

## Project Structure

- `docker-compose.yml`: Defines the Docker Compose setup for the project.

- `Dockerfile`: Contains instructions for building the Apache Spark image.

- `scripts/producer.py`: Python script to fetch financial data from Yahoo Finance WebSocket and send it to Kafka.

- `scripts/consumer.py`: Python script to consume data from Kafka, process it using Spark Structured Streaming

, and store it in Cassandra.

- `start-spark.sh`: Script to run Spark with the specified role (master or worker).

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements.
