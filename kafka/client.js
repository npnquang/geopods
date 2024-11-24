const axios = require('axios');

// Kafka REST Proxy configuration
const KAFKA_REST_URL = "http://localhost:8082";
const CONSUMER_GROUP = "js-group";
const CONSUMER_INSTANCE = "js-instance";
const TOPIC = "respond";
const POLL_INTERVAL = 500; // Polling interval in milliseconds
const BASE_URI = `${KAFKA_REST_URL}/consumers/${CONSUMER_GROUP}/instances/${CONSUMER_INSTANCE}` 

// Function to create a consumer
async function createConsumer() {
    const url = `${KAFKA_REST_URL}/consumers/${CONSUMER_GROUP}`;
    const payload = {
        "name": CONSUMER_INSTANCE,
        "format": "json",
        "auto.offset.reset": "earliest",
    };

    const headers = {
        "Content-Type": "application/vnd.kafka.v2+json",
    };

    const response = await axios.post(url, payload, { headers });
}

// Function to subscribe the consumer to a topic
async function subscribeToTopic(baseUri, topic) {
    const url = `${baseUri}/subscription`;
    const payload = { topics: [topic] };

    const headers = {
        "Content-Type": "application/vnd.kafka.v2+json",
    };

    await axios.post(url, payload, { headers });
}

// Function to consume messages from a topic
async function consumeMessages(baseUri) {
    const url = `${baseUri}/records`;
    const headers = {
        "Accept": "application/vnd.kafka.json.v2+json",
    };

    try {
        const response = await axios.get(url, { headers, timeout: 5000 });
        return response.data; // Returns the list of records
    } catch (error) {
        if (error.response && error.response.status === 404) {
            return []; // No new records
        }
        throw error;
    }
}

// Main function to manage the consumer lifecycle
async function main() {
    try {
        console.log("Creating consumer...");
        await createConsumer();

        await subscribeToTopic(BASE_URI, TOPIC);
        console.log(`Subscribed to topic '${TOPIC}'`);

        console.log("Polling for messages...");
        setInterval(async () => {
            try {
                const messages = await consumeMessages(BASE_URI);
                for (const record of messages) {
                    console.log("Received message:", record.value);
                }
            } catch (error) {
                console.error("Error while consuming messages:", error.message);
            }
        }, POLL_INTERVAL);
    } catch (error) {
        console.error("Error in consumer lifecycle:", error.message);
    }
}

main();
