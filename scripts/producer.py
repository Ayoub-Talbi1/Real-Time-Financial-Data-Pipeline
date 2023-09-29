import yliveticker
import json
from pykafka import KafkaClient
def initialize_kafka_producer():
    KAFKA_BROKER_ADDRESS = "kafka-container:9092"  # Update with your Kafka broker address
    KAFKA_TOPIC = "yfinance"

    client = KafkaClient(hosts=KAFKA_BROKER_ADDRESS)
    topic = client.topics[KAFKA_TOPIC]
    producer = topic.get_sync_producer()
    return producer
def on_new_msg(ws, msg):
    # Create a Kafka producer
    producer = initialize_kafka_producer()

    try:
        # Encode the message as a JSON string
        msg_json = json.dumps(msg)

        # Send the JSON-encoded message to the Kafka topic
        producer.produce(msg_json.encode('utf-8'))
        print(f"Message sent to Kafka: {msg_json}")
    except Exception as e:
        print(f"Error sending message to Kafka: {str(e)}")
    finally:
        producer.stop()
yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=[
    "SOL-USD", "BTC-USD", "ETH-USD", "XRP-USD", "DOGE-USD"])
