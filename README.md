# Widget Request Consumer

Install the Python dependencies with:

```
pip install -r requirements.txt
```

## Running the program

The request bucket is required:

```
python main.py --request-bucket <request-bucket>
```

To store processed widgets in S3:

```
python main.py 
  --request-bucket <request-bucket> 
  --store s3 
  --target-bucket <target-bucket>
```

To store processed widgets in DynamoDB:

```
python main.py 
  --request-bucket <request-bucket> 
  --store dynamodb 
  --table-name <table-name>
```

The consumer checks the request bucket continuously. Press Ctrl+C to stop
it. Processing messages are written to consumer.log.

## Command-line options

| Option | Description |
| --- | --- |
| `-rb`, `--request-bucket` | S3 bucket containing incoming request JSON files |
| `-s`, `--store` | Storage destination: `s3` or `dynamodb` |
| `--target-bucket` | Destination S3 bucket when using `--store s3` |
| `--table-name` | Destination DynamoDB table when using `--store dynamodb` |
| `-p`, `--profile` | AWS profile option |
| `-r`, `--region` | AWS region option |


## Running tests

Run the test suite with:

```
pytest
```
