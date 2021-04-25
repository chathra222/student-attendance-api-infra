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

    # Call compare faces API
    compare_faces_status = requests.post(
        "https://d6otawvpj7.execute-api.us-east-1.amazonaws.com/dev/compare-faces",
        json={
            "srcBucket": "student-faces-source",
            "sourceName": params["targetName"],
            "targetBucket": params["targetBucket"],
            "targetName": params["targetName"],
            "userId": params["userId"],
        },
        headers={"Content-type": "application/json"},
    )
    print(compare_faces_status)

    # Rest call to populate student table (add student attendance)
    add_student_attendance_status = requests.post(
        "https://d6otawvpj7.execute-api.us-east-1.amazonaws.com/dev/add-student-attdendance",
        json={
            "attendance_id": params["attendance_id"],
            "student_id": params["student_id"],
            "attended_time": params["attended_time"],
            "attended": params["attended"],
            "class_id": params["class_id"],
        },
        headers={"Content-type": "application/json"},
    )

    print(add_student_attendance_status)

    # if matched
    # Rest call to populate student_attendance_tab with 1
    # else no update
    body = {
        "message": "",
        "studentId": params["student_id"],
        "faceMatches": "false",
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body, default=dateconverter),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }

    return response


def dateconverter(o):
    print(type(o))
    if isinstance(o, datetime.datetime):
        return o.__str__()