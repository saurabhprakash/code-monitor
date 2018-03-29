import json

from django.conf import settings

import kafka

producer = kafka.KafkaProducer(bootstrap_servers=settings.KAFKA_ADDRESS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = kafka.KafkaConsumer(bootstrap_servers=settings.KAFKA_ADDRESS,
    value_deserializer=lambda m: json.loads(m.decode('ascii')))

# Assign a topic
topic = settings.KAFKA_TOPIC
consumer.subscribe([topic])

class Producer:
    
    def produce(self, payload):
        producer.send(topic, payload)


class Consumer:
    
    def consumer(self):
        while True:
            for message in consumer:
                #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                #message.offset, message.key, message.value))
                pass
