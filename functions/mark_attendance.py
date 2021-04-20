import json
import logging
import os
import boto3
from botocore.vendored import requests

# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    params = json.loads(event["body"])

    if "srcBucket" not in params or "sourceName" not in params:
        logger.error("Validation failed. Missing parameters")
        raise Exception("Missing parameters")
    # Call compare faces API

    # Rest call to populate student table

    # if matched
    # Rest call to populate student_attendance_tab with 1
    # else no update

    return response
