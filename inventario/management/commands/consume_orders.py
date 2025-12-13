from django.core.management.base import BaseCommand
import pika
import ssl
import json

class Command(BaseCommand):
    help = "Consume order events from RabbitMQ"

    def handle(self, *args, **options):
        context = ssl.create_default_context()

        credentials = pika.PlainCredentials(
            username="admin",
            password="martinez1234"
        )

        parameters = pika.ConnectionParameters(
            host="b-a2b574a6-48e2-47bb-966d-0af19418a9c4.mq.us-east-1.on.aws",
            port=5671,
            virtual_host="/",
            credentials=credentials,
            ssl_options=pika.SSLOptions(context)
        )

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.exchange_declare(
            exchange="order_events",
            exchange_type="fanout",
            durable=True
        )

        channel.queue_declare(
            queue="inventory.order.created",
            durable=True
        )

        channel.queue_bind(
            exchange="order_events",
            queue="inventory.order.created"
        )

        self.stdout.write(
            self.style.SUCCESS("🟢 Inventory Service conectado a RabbitMQ")
        )

        def callback(ch, method, properties, body):
            event = json.loads(body)
            self.stdout.write(f"📦 Evento recibido: {event}")

        channel.basic_consume(
            queue="inventory.order.created",
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()
