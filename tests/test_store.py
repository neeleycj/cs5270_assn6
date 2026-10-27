import pytest
import boto3
from moto import mock_aws
from consumer.store import S3Storage, DynamoDBStorage
from consumer.models import WidgetRequest
import json


@mock_aws
def test_s3_store():
    
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="test-bucket")
    test_widget = WidgetRequest(request_id=1, widget_type='type1', widget_id=1, owner='owner1', label='label1', description='desc1', other_attributes={})
    s3_store = S3Storage("test-bucket", s3)
    s3_store.store(test_widget)

    response = s3.get_object(Bucket="test-bucket", Key="widgets/owner1/1")

    content = response['Body'].read().decode('utf-8')
    assert json.loads(content) == {
        'request_id': 1,
        'widget_type': 'type1',
        'widget_id': 1,
        'owner': 'owner1',
        'label': 'label1',
        'description': 'desc1',
        'other_attributes': {}
    }

@mock_aws
def test_DDB_store():
    DDB = boto3.resource("dynamodb", region_name="us-east-1")
    table = DDB.create_table(
        TableName="test-table",
        KeySchema=[
            {
                'AttributeName': 'request_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'request_id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    test_widget = WidgetRequest(request_id=1, widget_type='type1', widget_id=1, owner='owner1', label='label1', description='desc1', other_attributes={'attr1': 'value1'})
    DDB_store = DynamoDBStorage("test-table", DDB)
    DDB_store.store(test_widget)

    response = table.get_item(Key={'request_id': 1})

    content = response['Item']
    assert content == {
        'request_id': 1,
        'widget_type': 'type1',
        'widget_id': 1,
        'owner': 'owner1',
        'label': 'label1',
        'description': 'desc1',
        'attr1': 'value1',
    }