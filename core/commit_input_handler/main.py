from core.commit_input_handler import kafka_util

class ProcessData:
    
    def push_data(self, payload):
        producer = kafka_util.Producer()
        producer.produce(payload)

    def run_consumer(self):
        consumer = kafka_util.Consumer()
        consumer.consume()