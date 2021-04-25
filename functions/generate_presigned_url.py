import json
import boto3
import logging
from botocore.client import Config
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    # s3 = boto3.client("s3", config=Config(s3={'addressing_style': 'path'},signature_version='s3v4'))
    s3 = boto3.client("s3", region_name="us-east-1")

    # expires_in = (datetime.now() +  datetime.timedelta(seconds=3600)  - datetime.datetime(1970,1,1)).total_seconds()
    params = json.loads(event["body"])
    print(event)
    # For fetching bucket_name & file_name using proxy integration method from API Gateway
    bucket_name = params["bucket"]
    file_name = params["fileName"]

    # For fetching bucket_name & file_name using legacy method from API Gateway
    # bucket_name = event["params"]["path"]["bucket"]
    # file_name = event["params"]["querystring"]["file"]

    """
    1. Generate pre-signed URL for downloading file
    2. Replace get_object with put_object for generating pre-signed URL to upload file
    3. Use PUT method while uploading file using Pre-Signed URL
    """

    URL = s3.generate_presigned_url(
        "put_object", Params={"Bucket": bucket_name, "Key": file_name}, ExpiresIn=3600
    )
    print(URL)
    """
    1. Generate pre-signed URL for downloading file
    2. Use POST method while uploading file using Pre-Signed URL
    """
    #  URL = s3.generate_presigned_post(Bucket=bucket_name, Key=file_name, Fields=None, Conditions=None, ExpiresIn=3600)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"URL": URL}),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }
