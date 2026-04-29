from botocore.exceptions import ClientError
import boto3

def connect_to_server(endpoint,id_key,secret_key):
    try:
        return boto3.client('s3',
                            endpoint_url=endpoint,
                            aws_access_key_id=id_key,
                            aws_secret_access_key=secret_key)
    except ClientError as e:
        raise ConnectionError(f"Client Error: {e.response['Error']['Message']}")
