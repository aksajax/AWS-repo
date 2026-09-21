import os
import uuid

import boto3
from dotenv import load_dotenv


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_file_to_s3(
    file,
    filename: str
):

    extension = filename.split(".")[-1]

    unique_filename = f"{uuid.uuid4()}.{extension}"

    s3_client.upload_fileobj(
        file,
        AWS_S3_BUCKET,
        unique_filename
    )

    return unique_filename