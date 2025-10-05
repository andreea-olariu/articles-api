import json
import os
import ssl

import pika
from dotenv import load_dotenv
from pika.exceptions import AMQPConnectionError
from retry import retry

load_dotenv()
ssl._create_default_https_context = ssl._create_unverified_context()


class RabbitMQWrapper:
    def __init__(self):
        self.connection_url = os.getenv('CLOUDAMQP_URL')
        self.publish_exchange = os.getenv('PUBLISH_EXCHANGE')
        self.publish_routing_key = os.getenv('PUBLISH_ROUTING_KEY')

        self.connection = None
        self.init_connection()

    def init_connection(self):
        params = pika.URLParameters(self.connection_url)

        self.connection = pika.BlockingConnection(params)

    @retry(AMQPConnectionError, delay=5, jitter=(1, 3))
    def publish_article(self, article: dict):
        if not self.connection:
            self.init_connection()

        channel = self.connection.channel()
        channel.basic_publish(exchange=self.publish_exchange, routing_key=self.publish_routing_key,
                              body=json.dumps(article))
