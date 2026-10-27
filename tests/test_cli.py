from consumer.cli import parse_args
import pytest

def test_correct_s3():
    test_args = ["-rb", "test-requests", "--store", "s3", "--target-bucket", "test-target"]
    args = parse_args(test_args)
    assert args.request_bucket == "test-requests"
    assert args.store == "s3"
    assert args.target_bucket  ==  "test-target"
def test_correct_DDB():
    test_args = ["-rb", "test-requests", "--store", "dynamodb", "--table-name", "test-table"]
    args = parse_args(test_args)
    assert args.request_bucket == "test-requests"
    assert args.store == "dynamodb"
    assert args.table_name  ==  "test-table"

def test_incorrect_args():
    test_args = ["-rb", "test-requests", "--store", "s3", "--target-bucket"]
    # args = parse_args(test_args)
    with pytest.raises(SystemExit):
        parse_args(test_args)