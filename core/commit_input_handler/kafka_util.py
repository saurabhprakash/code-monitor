import json

from django.conf import settings

import kafka


from core import models as core_models

producer = kafka.KafkaProducer(bootstrap_servers=settings.KAFKA_ADDRESS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    max_request_size=settings.KAFKA_MAX_REQUEST_SIZE, buffer_memory=settings.KAFKA_MAX_REQUEST_SIZE)
consumer = kafka.KafkaConsumer(bootstrap_servers=settings.KAFKA_ADDRESS,
    value_deserializer=lambda m: json.loads(m.decode('ascii')))

# Assign a topic
topic = settings.KAFKA_TOPIC
consumer.subscribe([topic])

class Producer:
    
    def produce(self, payload):
        future = producer.send(topic, payload)
        result = future.get(timeout=123)


class Consumer:
    
    def consume(self):
        while True:
            for message in consumer:
                core_models.CommitData.add_data(message.value.get('project'),
                    message.value.get('lint_report'), message.value.get('total_changes'),
                    message.value.get('email'), message.value.get('username'))
