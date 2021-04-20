import boto3
import json
import logging
import os


# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


poolId = "us-east-1_wYIgs9wnk"
clientId = "3rbb9pn62nncdbc0q19akncars"


def handler(event, context):
    params = json.loads(event["body"])
    congito_client = boto3.client("cognito-idp", region_name="us-east-1")
    response = congito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=clientId,
        AuthParameters={"USERNAME": params["username"], "PASSWORD": params["password"]},
    )
    print(response)
    if "ChallengeName" in response:
        body = {"session": response["Session"], "username": params["username"]}
        response = {"statusCode": 200, "body": json.dumps(body)}
    else:
        body = {"statusCode": 200, "body": response["AuthenticationResult"]}
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
