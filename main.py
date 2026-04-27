import boto3
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

bucket_name = "my-bucket"

def create_client():
    try:
        return boto3.client(
            "s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id=os.getenv("ACCESS_KEY"),
            aws_secret_access_key=os.getenv("SECRET_KEY"),
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create S3 client: {e}")


def ensure_bucket(client):
    try:
        client.head_bucket(Bucket=bucket_name)
        print("Bucket already exists")

    except Exception:
        try:
            client.create_bucket(Bucket=bucket_name)
            print("Bucket created")
        except Exception as e:
            raise RuntimeError(f"Failed to create bucket: {e}")

    try:
        client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={"Status": "Enabled"}
        )
        print("Versioning enabled")
    except Exception as e:
        raise RuntimeError(f"Failed to enable versioning: {e}")


def random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ".txt"


def random_data():
    return ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(20, 200)
    ))


def list_objects(client):
    try:
        response = client.list_objects_v2(Bucket=bucket_name)

        if "Contents" not in response:
            print("No objects found")
            return []

        objects = response["Contents"]

        print("\nObjects:")
        for i, obj in enumerate(objects):
            print(f"{i}: {obj['Key']}")

        return objects

    except Exception as e:
        raise RuntimeError(f"Failed to list objects: {e}")


def select_object(client):
    objects = list_objects(client)

    if not objects:
        raise ValueError("No objects available")

    try:
        index = int(input("Choose index: "))

        if index < 0 or index >= len(objects):
            raise IndexError("Invalid index")

        return objects[index]["Key"]

    except ValueError:
        raise ValueError("Index must be a number")


def put_object(client, mode="create"):
    try:
        if mode == "create":
            name = random_name()
        else:
            name = select_object(client)

        data = random_data()

        client.put_object(
            Bucket=bucket_name,
            Key=name,
            Body=data.encode()
        )

        print(f"{mode.capitalize()} done: {name}")

    except Exception as e:
        raise RuntimeError(f"Failed to {mode} object: {e}")


def read_object(client):
    try:
        name = select_object(client)

        response = client.get_object(
            Bucket=bucket_name,
            Key=name
        )

        data = response["Body"].read().decode()

        print("\nContent:")
        print(data)

    except Exception as e:
        raise RuntimeError(f"Failed to read object: {e}")


def delete_object(client):
    try:
        name = select_object(client)

        client.delete_object(
            Bucket=bucket_name,
            Key=name
        )

        print(f"Deleted (delete marker added if versioning is enabled): {name}")

    except Exception as e:
        raise RuntimeError(f"Failed to delete object: {e}")


def show_versions(client):
    try:
        response = client.list_object_versions(Bucket=bucket_name)

        print("\nVersions:")
        for v in response.get("Versions", []):
            print(
                f"Key: {v['Key']} | VersionId: {v['VersionId']} | Latest: {v['IsLatest']}"
            )

    except Exception as e:
        raise RuntimeError(f"Failed to list versions: {e}")


def menu():
    client = create_client()
    ensure_bucket(client)

    actions = {
        "1": lambda c: put_object(c, "create"),
        "2": list_objects,
        "3": read_object,
        "4": delete_object,
        "5": lambda c: put_object(c, "update"),
        "7": show_versions
    }

    while True:
        print("""
        1 Create
        2 List
        3 Read
        4 Delete
        5 Update
        6 Exit
        7 Show Versions 
        """)

        choice = input("Choose: ")

        if choice == "6":
            break

        action = actions.get(choice)

        if action:
            action(client)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()