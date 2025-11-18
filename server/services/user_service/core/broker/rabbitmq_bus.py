import pika
import json

class RabbitMQEventBus:
    def __init__(self, host='localhost'):
        self.host = host

    def _connect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.host))

    def publish(self, event_type: str, data: dict):
        """Send event to RabbitMQ queue"""
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=event_type, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=event_type,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)  # persistent
        )
        connection.close()
        print(f"Published event '{event_type}' with data: {data}")

    def subscribe(self, event_type: str, callback):
        """Listen to a queue and call the callback"""
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=event_type, durable=True)

        def wrapper(ch, method, properties, body):
            data = json.loads(body)
            callback(event_type, data)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=event_type, on_message_callback=wrapper)

        print(f"Listening for '{event_type}' events...")
        channel.start_consuming()
        
