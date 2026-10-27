import argparse

def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='ConsumerProgram')
    parser.add_argument('-s','--store', choices=['s3', 'dynamodb'])
    parser.add_argument('--target-bucket')
    parser.add_argument('--table-name')
    parser.add_argument('-p', '--profile')
    parser.add_argument('-r', '--region')
    parser.add_argument('-rb', '--request-bucket')
    parser.add_argument('-mrt', '--max-runtime')
    parsed  = parser.parse_args(args)

    if parsed.store == 's3' and not parsed.target_bucket:
        parser.error("The --target-bucket argument is required when --store is 's3'.")
    if parsed.store == 'dynamodb' and not parsed.table_name:
        parser.error("The --table-name argument is required when --store is 'dynamodb'.")
    return parsed