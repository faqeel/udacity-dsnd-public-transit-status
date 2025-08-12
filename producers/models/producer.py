"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    TOPIC_PREFIX = "org.chicago.cta"

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            'bootstrap.servers': 'PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094',
            'schema.registry.url': 'http://localhost:8081'
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer(
            self.broker_properties,
            default_key_schema=self.key_schema,
            default_value_schema=self.value_schema
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        admin_client = AdminClient({"bootstrap.servers": self.broker_properties["bootstrap.servers"]})

        # Get cluster metadata
        topic_metadata = admin_client.list_topics(timeout=5)

        if self.topic_name in topic_metadata.topics:
            logger.debug(f"Topic {self.topic_name} already exists")
            return

        # Create topic
        new_topic = NewTopic(
            topic=self.topic_name,
            num_partitions=self.num_partitions,
            replication_factor=self.num_replicas
        )

        # Create topic on broker
        futures = admin_client.create_topics([new_topic])

        for topic, future in futures.items():
            try:
                future.result()  # The result itself is None
                logger.info(f"Topic {topic} created successfully")
            except Exception as e:
                logger.error(f"Failed to create topic {topic}: {e}")

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        if self.producer is not None:
            self.producer.flush()
        logger.info("Producer closed successfully")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
