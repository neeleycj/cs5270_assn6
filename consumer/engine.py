import time
import logging

class Engine:
    def __init__(self, receiver, storage, max_iteration=None):
        self.receiver = receiver
        self.storage = storage

    def run(self):
        logger = logging.getLogger(__name__)
        try:
            while True:
                logger.info("Checking for new requests...")
                req = self.receiver.get_next_request()
                if req is not None:
                    logger.info(f"Received request: {req.request_id}")
                    self.storage.store(req)
                    logger.info(f"Stored request: {req.request_id}")
                else:
                    logger.info("No new requests found. Waiting for 0.1 seconds before checking again.")
                    time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user.")