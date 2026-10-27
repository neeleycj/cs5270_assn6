import pytest
import boto3
from moto import mock_aws
from consumer.receivers import S3RequestReceiver
import json


@mock_aws
def test_receive():
    testing_req = {
        "Contents":
            [{
                "Key": "test.json"
            }]
    }

    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="test/test.txt", Body=json.dumps(testing_req))

    receiver = S3RequestReceiver("test-bucket", s3)

    req = receiver.get_next_request()

    assert req == testing_req

@mock_aws
def test_no_widgets():
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")

    receiver = S3RequestReceiver("test-bucket", s3)
    
    req = receiver.get_next_request()

    assert req == None