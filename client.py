from s3_service import S3Service
from connection import connect_to_server
from utils import build_bucket_name
from pathlib import Path
from dotenv import load_dotenv
from config import ENDPOINT_URL
import os

if __name__ == '__main__':
    env_path = Path('.') / '.env.exam'
    load_dotenv(dotenv_path=env_path)
    try:
        conn_s3 = connect_to_server(ENDPOINT_URL,os.getenv("S3_ACCESS_KEY"),os.getenv("S3_SECRET_KEY"))
        bucket_name = build_bucket_name()
        s3_service = S3Service(conn_s3, bucket_name)
        operations = {
            1: s3_service.create_object,
            2: s3_service.list_existing_objects,
            3: s3_service.read_data_from_object,
            4: s3_service.remove_object,
            5: s3_service.update_object
        }

        while True:
            print("\nPlease enter your choice:")
            print("1: Create an object")
            print("2: List objects")
            print("3: Read object")
            print("4: Remove object")
            print("5: Update object")
            print("0: Exit")

            action = int(input(">> "))
            if action == 0:
                break
            operation = operations.get(action)
            if operation:
                operation()
            else:
                print("Invalid choice")

    except Exception as e:
        print(f"Error: {e}")

