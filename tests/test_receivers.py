import pytest
import boto3
from moto import mock_aws

from consumer.receivers import S3RequestReceiver, SQSRequestReceiver
import json


@mock_aws
def test_receive_s3():
    testing_req = {
            "requestId": 1,
            "type": "create",
            "widgetId": 1,
            "owner": "test1",
            "label": "test1",
            "description": "test1",
            "otherAttributes": {"test1": "test1"}
        }
    confirmation_req = {
        "request_id": 1,
        "widget_type": "create",
        "widget_id": 1,
        "owner": "test1",
        "label": "test1",
        "description": "test1",
        "other_attributes": {"test1": "test1"}
    }

    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="test/test.txt", Body=json.dumps(testing_req))

    receiver = S3RequestReceiver("test-bucket", s3)

    req = receiver.get_next_request()
    req = req.to_dict()

    assert req == confirmation_req

@mock_aws
def test_receive_sqs():
    testing_req = {
        "requestId": 1,
        "type": "create",
        "widgetId": 1,
        "owner": "test1",
        "label": "test1",
        "description": "test1",
        "otherAttributes": {"test1": "test1"}
    }
    confirmation_req = {
        "request_id": 1,
        "widget_type": "create",
        "widget_id": 1,
        "owner": "test1",
        "label": "test1",
        "description": "test1",
        "other_attributes": {"test1": "test1"}
    }

    sqs = boto3.client("sqs")
    sqs.create_queue(QueueName="test-queue")
    queue_url = sqs.get_queue_url(QueueName="test-queue")["QueueUrl"]
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(testing_req))

    receiver = SQSRequestReceiver("test-queue", sqs)

    req = receiver.get_next_request()
    req = req.to_dict() 
    assert req == confirmation_req

@mock_aws
def test_no_widgets_s3():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")

    receiver = S3RequestReceiver("test-bucket", s3)
    
    req = receiver.get_next_request()

    assert req == None

@mock_aws
def test_no_widgets_sqs():
    sqs = boto3.client("sqs")
    sqs.create_queue(QueueName="test-queue")

    receiver = SQSRequestReceiver("test-queue", sqs)
    
    req = receiver.get_next_request()

    assert req == None