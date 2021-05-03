import json
import logging
import os
import datetime
from botocore.vendored import requests
import boto3

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
            "userId": params["student_id"],
        },
        headers={"Content-type": "application/json"},
    )
    print(compare_faces_status.text)
    compare_faces_response = compare_faces_status.text
    compare_faces_response_dict_obj = json.loads(compare_faces_response)
    print(compare_faces_response_dict_obj["faceMatches"])

    if compare_faces_response_dict_obj["faceMatches"] == "true":
        # Rest call to populate student table (add student attendance)
        add_student_attendance_status = requests.post(
            "https://d6otawvpj7.execute-api.us-east-1.amazonaws.com/dev/add-student-attendance",
            json={
                "attendance_id": params["attendance_id"],
                "student_id": params["student_id"],
                "attended_time": params["attended_time"],
                "attended": compare_faces_response_dict_obj["faceMatches"],
                "class_id": params["class_id"],
            },
            headers={"Content-type": "application/json"},
        )
        print(add_student_attendance_status.text)

        # if matched
        # Rest call to populate student_attendance_tab with 1
        # else no update
        body = {
            "message": "Student face Matches",
            "studentId": params["student_id"],
            "faceMatches": compare_faces_response_dict_obj["faceMatches"],
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
    else:
        body = {
            "message": "Student face not found in database",
            "studentId": params["student_id"],
            "faceMatches": compare_faces_response_dict_obj["faceMatches"],
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