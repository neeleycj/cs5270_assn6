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
        body  = json.dumps(widget.to_dict())
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=body)

    def update(self, widget):
        try:
            key = widget.s3_key_generator()
            body  = json.dumps(widget.to_dict())
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=body)
        except Exception as e:
            print(f"Error updating widget: {e}")

    def delete(self, widget):
        try:
            key = widget.s3_key_generator()
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except Exception as e:
            print(f"Error deleting widget: {e}")

class DynamoDBStorage:
    def __init__(self, table_name, DDB=boto3.resource('dynamodb', region_name='us-east-1')):
        self.table_name = table_name
        self.DDB = DDB

    def store(self, widget):
        dict = widget.dynamoDB_formatter()
        table = self.DDB.Table(self.table_name)
        table.put_item(Item=dict)

    def update(self, widget):
        try:
            dict = widget.dynamoDB_formatter()
            table = self.DDB.Table(self.table_name)
            table.put_item(Item=dict)
        except Exception as e:
            print(f"Error updating widget: {e}")
            
    def delete(self, widget):
        try:
            dict = widget.dynamoDB_formatter()
            table = self.DDB.Table(self.table_name)
            table.delete_item(Key={'request_id': dict['request_id']})
        except Exception as e:
            print(f"Error deleting widget: {e}")
