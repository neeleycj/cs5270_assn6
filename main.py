import logging
from consumer.cli import parse_args
import consumer.engine
import consumer.receivers
import consumer.store

def main():
    logging.basicConfig(filename="consumer.log", level=logging.INFO)
    receiver = consumer.receivers.S3RequestReceiver(args.request_bucket)
    storage = ''
    if args.target_bucket:
        storage = consumer.store.S3Storage(args.target_bucket)
    if args.table_name:
            storage = consumer.store.DynamoDBStorage(args.table_name)
    engine = consumer.engine.Engine(receiver, storage)
    engine.run()
    

if __name__ == "__main__":
    args = parse_args()
    main()