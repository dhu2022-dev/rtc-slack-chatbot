import boto3
import json

class S3Manager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def read_json_from_s3(self, object_key):
        """Read a JSON file from S3 and return its contents."""
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
        data = json.loads(response["Body"].read().decode("utf-8"))
        return data

    def write_to_s3(self, object_key, data):
        """Write data to S3 as a JSON file."""
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=object_key,
            Body=json.dumps(data, indent=4),
            ContentType="application/json"
        )

    def list_files_in_directory(self, prefix):
        """List all files in the given S3 directory."""
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")]
