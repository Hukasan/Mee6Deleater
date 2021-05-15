import boto3
import botocore
import json
from pprint import pprint
from os import environ

access_key = str(environ["AWS_ACCESS_KEY_ID"])
secret_key = str(environ["AWS_SECRET_ACCESS_KEY"])
bucket_name = str(environ["AWS_BUCKET_NAME"])
s3 = boto3.resource(
    service_name="s3", region_name="ap-northeast-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key
).Bucket(bucket_name)


class json_io_s3:
    def __init__(self, name: str):
        folder_name = "mee6deleter"
        self.key = folder_name + "/" + name + ".json"
        self.obj = s3.Object(self.key)

    def put(self, data: dict):
        _ = self.obj.put(Body=json.dumps(data, ensure_ascii=False, indent=2))

    def get(self):
        return json.load(self.obj.get()["Body"])


if __name__ == "__main__":
    name = "setup"
    with open("testfolder/" + name + ".json") as f:
        data = json.load(f)
        target = json_io_s3(name)
        target.put(data)
        print(target.get())
