import json
import logging
import os
from botocore.vendored import requests
import boto3

# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# add a user in cognito pool
poolId = "us-east-1_wYIgs9wnk"


def handler(event, context):
    params = json.loads(event["body"])
    congito_client = boto3.client("cognito-idp", region_name="us-east-1")
    if params["type"] == "student":
        response = congito_client.admin_create_user(
            UserPoolId=poolId,
            Username=params["student_id"],
            TemporaryPassword="Tempp@ss123",
            UserAttributes=[{"Name": "email", "Value": params["email"]}],
        )
        body = {
            "message": "Student User Created in cognito",
            "username": params["student_id"],
        }
        # Rest call to populate student table
        status = requests.post(
            "https://d6otawvpj7.execute-api.us-east-1.amazonaws.com/dev/add-student",
            json={
                "student_id": params["student_id"],
                "email": params["email"],
                "phone": params["phone"],
                "f_name": params["f_name"],
                "l_name": params["l_name"],
                "district": params["district"],
                "source_image_key": params["source_image_key"],
                "dob": params["dob"],
                "course_id": params["course_id"],
                "type": "student",
            },
            headers={"Content-type": "application/json"},
        )
        print(status)
    elif params["type"] == "lecturer":
        response = congito_client.admin_create_user(
            UserPoolId=poolId,
            Username=params["lecturer_id"],
            TemporaryPassword="Tempp@ss123",
            UserAttributes=[{"Name": "email", "Value": params["email"]}],
        )
        body = {
            "message": "Lectuer User Created in cognito",
            "username": params["lecturer_id"],
        }
        # Rest Call to add user api
        status = requests.post(
            "https://d6otawvpj7.execute-api.us-east-1.amazonaws.com/dev/add-lecturer",
            json={
                "lecturer_id": params["lecturer_id"],
                "email": params["email"],
                "mobile": params["mobile"],
                "f_name": params["f_name"],
                "l_name": params["l_name"],
                "gender": params["gender"],
                "type": "lecturer",
            },
            headers={"Content-type": "application/json"},
        )
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }
    return response
