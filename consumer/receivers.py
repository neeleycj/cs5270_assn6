import abc
import boto3
import json
import collections
from consumer.models import WidgetRequest

class RequestReceiver:
    @abc.abstractmethod
    def get_next_request(self):
        pass

class S3RequestReceiver(RequestReceiver):

    def __init__(self, bucket_name, s3_client=boto3.client('s3')):
        self.bucket_name =  bucket_name
        self.s3_client = s3_client

    def get_next_request(self):
        res = self.s3_client.list_objects_v2(Bucket=self.bucket_name, MaxKeys = 1)
        if 'Contents' not in res or res['Contents'] is None:
            return None

        key = res['Contents'][0]['Key']

        object = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        raw_string = object['Body'].read().decode('utf-8')
        parsed = json.loads(raw_string)
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        return WidgetRequest.from_dict(parsed)

class SQSRequestReceiver(RequestReceiver):
    def __init__(self, queue_name, sqs_client=boto3.client('sqs')):
        self.queue_name = queue_name
        self.sqs_client = sqs_client
        self.queue_url = self.sqs_client.get_queue_url(QueueName=self.queue_name)['QueueUrl']
        self.cache = collections.deque()

    def get_next_request(self):
        if not self.cache:
            response = self.sqs_client.receive__message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']