import abc
import boto3
import json

class Storage:
    @abc.abstractmethod
    def store(self, widget):
        pass
    @abc.abstractmethod
    def update(self, widget):
        pass
    @abc.abstractmethod
    def delete(self, widget):
        pass

class S3Storage(Storage):
    def __init__(self, bucket_name, s3_client=boto3.client('s3')):
        self.bucket_name =  bucket_name
        self.s3_client = s3_client
    def store(self, widget):
        key = widget.s3_key_generator()
        body  = json.dumps(widget)
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=body)

class DynamoDBStorage:
    def __init__(self, table_name, DDB=boto3.resource('dynamodb')):
        self.table_name = table_name
        self.DDB = DDB

    def store(self, widget):
        dict = widget.dynamoDB_formatter()
        table = self.DDB.Table(self.table_name)
        self.DDB.put_item(Item=dict)