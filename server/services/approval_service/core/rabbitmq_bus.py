import pika
import json

class RabbitMQEventBus:
    def __init__(self, host='localhost'):
        self.host = host

    def _connect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.host))

    def publish(self, topic: str, data: dict):
        """Send event to RabbitMQ queue"""
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=topic, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=topic,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )
        connection.close()
        print(f"Published event '{topic}' with data: {data}")   

    def subscribe(self, topic: str, callback):
        """Listen to a queue and call the callback"""
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=topic, durable=True)

        def wrapper(ch, method, properties, body):
            data = json.loads(body)
            callback(topic, data)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=topic, on_message_callback=wrapper)

        print(f"Listening for '{topic}' events...")
        channel.start_consuming()
        
