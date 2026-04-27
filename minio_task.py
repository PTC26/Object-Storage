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
        s3.list_buckets() 
        return s3
    except ClientError as e:
        raise ConnectionError(f"MinIO Client Error: {e.response['Error']['Message']}")
    except Exception as e:
        raise ConnectionError(f"Unexpected connection error: {e}")

def ensure_bucket(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            s3.create_bucket(Bucket=bucket_name)
        else:
            raise RuntimeError(f"Could not verify bucket: {e.response['Error']['Message']}")

def handle_create(s3, bucket_name, last_file=None):
    try:
        size = random.randint(20, 150)
        filename = f"file_{uuid.uuid4().hex[:6]}.txt"
        content = "".join(random.choices(string.ascii_letters + string.digits, k=size))
        s3.put_object(Bucket=bucket_name, Key=filename, Body=content.encode())
        return filename 
    except ClientError as e:
        raise RuntimeError(f"Upload failed: {e.response['Error']['Message']}")

def handle_list(s3, bucket_name, last_file=None):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        return response.get('Contents', [])
    except ClientError as e:
        raise RuntimeError(f"Listing failed: {e.response['Error']['Message']}")

def handle_read(s3, bucket_name, last_file=None):
    target = input(f"File to read [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    try:
        response = s3.get_object(Bucket=bucket_name, Key=target)
        return response['Body'].read().decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise FileNotFoundError(f"Object '{target}' not found.")
        raise RuntimeError(f"Read failed: {e.response['Error']['Message']}")

def handle_update(s3, bucket_name, last_file=None):
    target = input(f"File to update [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    try:
        s3.head_object(Bucket=bucket_name, Key=target)
        new_content = f"Update {uuid.uuid4().hex[:4]} | " + "".join(random.choices(string.ascii_letters, k=30))
        s3.put_object(Bucket=bucket_name, Key=target, Body=new_content.encode())
        return target
    except ClientError as e:
        raise RuntimeError(f"Update failed: {e.response['Error']['Message']}")

def handle_remove(s3, bucket_name, last_file=None):
    target = input(f"File to remove [{last_file}]: ") or last_file
    if not target: raise ValueError("No file selected.")
    try:
        s3.head_object(Bucket=bucket_name, Key=target)
        s3.delete_object(Bucket=bucket_name, Key=target)
        return target
    except ClientError as e:
        raise RuntimeError(f"Removal failed: {e.response['Error']['Message']}")

def main():
    bucket_name = os.getenv("MINIO_BUCKET")
    s3 = None
    
    try:
        s3 = get_s3_client()
        ensure_bucket(s3, bucket_name)
        print(f"[*] Connected to {bucket_name} successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return

    last_file = None

    while True:
        print("\n1. Create | 2. List | 3. Read | 4. Update | 5. Remove | 6. Exit")
        choice = input("Select an option: ")

        if choice == '6':
            print("Exiting...")
            break

        actions = {
            '1': lambda: handle_create(s3, bucket_name),
            '2': lambda: handle_list(s3, bucket_name),
            '3': lambda: handle_read(s3, bucket_name, last_file),
            '4': lambda: handle_update(s3, bucket_name, last_file),
            '5': lambda: handle_remove(s3, bucket_name, last_file)
        }

        func = actions.get(choice)
        
        if func:
            try:
                result = func()
                
                if choice == '1':
                    last_file = result
                    print(f"[V] Created: {last_file}")
                elif choice == '2':
                    if not result:
                        print("Bucket is empty.")
                    else:
                        print("Bucket objects:")
                        for obj in result:
                            print(f" - {obj['Key']} ({obj['Size']} bytes)")
                elif choice == '3':
                    print(f"Content: {result}")
                elif choice == '4':
                    print(f"[V] Updated object: {result}")
                elif choice == '5':
                    print(f"[V] Removed: {result}")
                    if result == last_file:
                        last_file = None
                        
            except (ClientError, ValueError, RuntimeError, FileNotFoundError, ConnectionError) as e:
                print(f"\n[!] Operation Failed: {e}")
            except Exception as e:
                print(f"\n[!] Unexpected system error: {e}")
        else:
            print("Invalid choice. Please try 1-6.")

if __name__ == "__main__":
    main()