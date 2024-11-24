import requests
import time

# Kafka REST Proxy configuration
KAFKA_REST_URL = "http://localhost:8082"
STREAM_TOPIC = "stream"
RESPOND_TOPIC = "respond"
CONSUMER_GROUP = "py-group"
CONSUMER_INSTANCE = "py-instance"
CONSUME_INTERVAL = 0.1  # Polling interval in seconds
BASE_URI = f'{KAFKA_REST_URL}/consumers/{CONSUMER_GROUP}/instances/{CONSUMER_INSTANCE}'


# Function to create a Kafka consumer
def create_consumer():
    url = f"{KAFKA_REST_URL}/consumers/{CONSUMER_GROUP}"
    payload = {
        "name": CONSUMER_INSTANCE,
        "format": "json",
        "auto.offset.reset": "earliest"
    }
    headers = {"Content-Type": "application/vnd.kafka.v2+json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

# Function to subscribe the consumer to a topic
def subscribe_to_topic(base_uri, topic):
    url = f"{base_uri}/subscription"
    payload = {"topics": [topic]}
    headers = {"Content-Type": "application/vnd.kafka.v2+json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

# Function to consume messages from a topic
def consume_messages(base_uri):
    url = f"{base_uri}/records"
    headers = {"Accept": "application/vnd.kafka.json.v2+json"}
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        return response.json()
    return []

# Function to produce messages to a topic
def produce_message(topic, message):
    url = f"{KAFKA_REST_URL}/topics/{topic}"
    payload = {"records": [{"value": message}]}
    headers = {"Content-Type": "application/vnd.kafka.json.v2+json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

# Main processing logic
def main():
    try:
        # Create consumer and subscribe to the stream topic
        create_consumer()
        subscribe_to_topic(BASE_URI, STREAM_TOPIC)

        print(f"Subscribed to topic '{STREAM_TOPIC}'")
        
        while True:
            # Consume messages from the stream topic
            messages = consume_messages(BASE_URI)
            print("__________________________________________________________")
            
            for record in messages:
                # Extract the message value
                input_message = record["value"]
                print(type(input_message))

                # Process the message (custom logic goes here)
                result = {
                    "output": input_message['data']['x'] + input_message['data']['y'],
                    "timestamp": time.time(),
                    "server_latency": time.time() - input_message["timestamp"]
                }
                
                # Produce the processed message to the respond topic
                produce_message(RESPOND_TOPIC, result)

            # Sleep before polling again
            # time.sleep(CONSUME_INTERVAL)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
