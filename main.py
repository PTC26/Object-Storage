from minio import Minio
from minio.error import S3Error
import random
import string
import io


bucket_name = "my-bucket"
def create_client(access_key, secret_key):
    return Minio(
        "localhost:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )


def ensure_bucket(client):
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print("Bucket created")
        else:
            print("Bucket already exists")
    except S3Error as e:
        print("Error:", e)


def random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ".txt"

def random_data():
    return ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(20, 200)
    ))


def put_object(client, mode="create"):
    try:
        if mode == "create":
            name = random_name()
        else:
            name = select_object(client)

        if not name:
            return

        data = random_data()

        client.put_object(
            bucket_name,
            name,
            data=io.BytesIO(data.encode()),
            length=len(data)
        )

        print(f"{mode.capitalize()} done: {name}")

    except S3Error as e:
        print("Error:", e)


def list_objects(client):
    objects = list(client.list_objects(bucket_name))

    if not objects:
        print("No objects found")
        return []

    print("\nObjects:")
    for i, obj in enumerate(objects):
        print(f"{i}: {obj.object_name}")

    return objects


def select_object(client):
    objects = list_objects(client)

    if not objects:
        return None

    index = int(input("Choose index: "))
    return objects[index].object_name


def read_object(client):
    try:
        name = select_object(client)
        if not name:
            return

        response = client.get_object(bucket_name, name)
        print("\nContent:")
        print(response.read().decode())

    except S3Error:
        print("Error reading object")


def delete_object(client):
    try:
        name = select_object(client)
        if not name:
            return

        client.remove_object(bucket_name, name)
        print(f"Deleted: {name}")

    except S3Error:
        print("Error deleting object")


def menu():
    print("LOGIN")
    access_key = input("Enter access key: ")
    secret_key = input("Enter secret key: ")

    client = create_client(access_key, secret_key)
    ensure_bucket(client)

    actions = {
        "1": lambda c: put_object(c, "create"),
        "2": list_objects,
        "3": read_object,
        "4": delete_object,
        "5": lambda c: put_object(c, "update")
    }

    while True:
        menu_text = """
        1 Create
        2 List
        3 Read
        4 Delete
        5 Update
        6 Exit
        """

        print(menu_text)

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