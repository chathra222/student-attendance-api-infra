import json
import logging
import os
import boto3

# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    params = json.loads(event["body"])

    if "srcBucket" not in params or "sourceName" not in params:
        logger.error("Validation failed. Missing parameters")
        raise Exception("Missing parameters")

    client = boto3.client("rekognition")

    data = client.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": params["srcBucket"],
                "Name": params["sourceName"],
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": params["targetBucket"],
                "Name": params["targetName"],
            }
        },
        SimilarityThreshold=95.0,
    )

    if len(data["FaceMatches"]) > 0:

        body = {
            "message": "Face is matching",
            "studentId": params["userId"],
            "faceMatches": "true",
        }
        # update student attendance table
        response = {"statusCode": 200, "body": json.dumps(body)}

        return response

    body = {
        "message": "Face is not matching",
        "studentId": params["userId"],
        "faceMatches": "false",
    }
    # update student attendance table
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
