from botocore.exceptions import ClientError
from utils import *
import uuid
class S3Service:
    def __init__(self, conn_s3, bucket_name):
        self.s3 = conn_s3
        self.bucket = bucket_name
        self.validate_bucket()

    # func 1
    def create_object(self):
        bucket = self.bucket
        obj_name = str(uuid.uuid4())
        obj_data = create_random_data()
        try:
            self.s3.put_object(Bucket=self.bucket, Key=obj_name, Body=obj_data)
            print(f"Object '{obj_name}' created successfully.")
        except ClientError as e:
            raise ConnectionError(f"Client Error: {e.response['Error']['Message']}")

    # func 2
    def list_existing_objects(self):
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket)
            objects_names = []
            if "Contents" in objects:
                for obj in objects["Contents"]:
                    objects_names.append(obj["Key"])
                print("Display list of exist objects.")
                for i, name in enumerate(objects_names):
                    print(f"{i}: {name}")
            return objects_names
        except Exception as e:
            print(f"Error listing objects: {e}")
            return []

    # func 3
    def read_data_from_object(self):
        selected_key = self.choose_object()
        if not selected_key:
            return
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=selected_key)
            data = response["Body"].read().decode()
            print(f"Data content: {data}")
            print(f"Object '{selected_key}' read successfully.")
        except ClientError as e:
            print(f"Error reading object: {e}")

    # func 4
    def remove_object(self):
        selected_key = self.choose_object()
        if not selected_key:
            return
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=selected_key)
            print(f"Object {selected_key} removed successfully.")
        except ClientError as e:
            print(f"Error removing object: {e}")

    # func 5
    def update_object(self):
        try:
            obj_for_update = self.choose_object()
            if obj_for_update:
                new_data = create_random_data()
                self.s3.put_object(
                    Bucket=self.bucket,
                    Key=obj_for_update,
                    Body=new_data
                )
                print(f"Object '{obj_for_update}' updated successfully.")
        except ClientError as e:
            print(f"Error updating object: {e}")

    def choose_object(self):
        objects = self.list_existing_objects()
        if not objects:
            print("No objects found.")
            return None
        try:
            index = int(input("Enter num of the selected object:"))
            return objects[index]
        except Exception as e:
            print("Invalid selection.")
            return None

    def validate_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
        except ClientError:
            try:
                self.s3.create_bucket(Bucket=self.bucket)
            except ClientError as e:
                raise ConnectionError(str(e))

        self.s3.put_bucket_versioning(
            Bucket=self.bucket,
            VersioningConfiguration={"Status": "Enabled"}
        )
