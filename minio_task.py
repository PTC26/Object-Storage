import os
import boto3
import uuid
import random
import string
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

def get_s3_client():
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=f"http://{os.getenv('MINIO_SERVER')}",
            aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
        )
        return s3
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MinIO: {e}")

def ensure_bucket(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)


def handle_create(s3, bucket_name, last_file=None):
    size = random.randint(20, 150)
    filename = f"file_{uuid.uuid4().hex[:6]}.txt"
    content = "".join(random.choices(string.ascii_letters + string.digits, k=size))
    s3.put_object(Bucket=bucket_name, Key=filename, Body=content.encode())
    print(f"[V] Created: {filename} ({size} bytes)")
    return filename

def handle_list(s3, bucket_name, last_file=None):
    response = s3.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])
    if not objects:
        print("Bucket is empty.")
    for obj in objects:
        print(f" - {obj['Key']} ({obj['Size']} bytes)")
    return last_file

def handle_read(s3, bucket_name, last_file=None):
    target = input(f"File to read [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    try:
        response = s3.get_object(Bucket=bucket_name, Key=target)
        content = response['Body'].read().decode('utf-8')
        print(f"Content: {content}")
    except ClientError:
        raise FileNotFoundError(f"The file '{target}' was not found.")
    return last_file

def handle_update(s3, bucket_name, last_file=None):
    target = input(f"File to update [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    s3.head_object(Bucket=bucket_name, Key=target)
    new_size = random.randint(20, 150)
    new_content = f"Update ID: {uuid.uuid4().hex[:4]} | " + "".join(random.choices(string.ascii_letters, k=new_size))
    s3.put_object(Bucket=bucket_name, Key=target, Body=new_content.encode())
    print(f"[V] Updated {target}. New size: {len(new_content)} bytes.")
    return last_file

def handle_remove(s3, bucket_name, last_file=None):
    target = input(f"File to remove [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    s3.head_object(Bucket=bucket_name, Key=target)
    s3.delete_object(Bucket=bucket_name, Key=target)
    print(f"[V] Removed {target}")
    return None if target == last_file else last_file


def main():
    bucket_name = os.getenv("MINIO_BUCKET")
    try:
        s3 = get_s3_client()
        ensure_bucket(s3, bucket_name)
        print(f"[*] Connected to {os.getenv('MINIO_SERVER')} successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return

    actions = {
        '1': handle_create,
        '2': handle_list,
        '3': handle_read,
        '4': handle_update,
        '5': handle_remove
    }

    last_file = None

    while True:
        print("\n1. Create | 2. List | 3. Read | 4. Update | 5. Remove | 6. Exit")
        choice = input("Select an option: ")

        if choice == '6':
            print("Exiting...")
            break

        action = actions.get(choice)
        if action:
            try:
                last_file = action(s3, bucket_name, last_file)
            except Exception as e:
                print(f"[!] Operation Failed: {e}")
        else:
            print("Invalid choice. Please try 1-6.")

if __name__ == "__main__":
    main()