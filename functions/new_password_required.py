import json
import logging
import os
import boto3


# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
clientId = "3rbb9pn62nncdbc0q19akncars"


def handler(event, context):
    params = json.loads(event["body"])
    congito_client = boto3.client("cognito-idp", region_name="us-east-1")
    response = congito_client.respond_to_auth_challenge(
        ChallengeName="NEW_PASSWORD_REQUIRED",
        Session=params["session"],
        ClientId=clientId,
        ChallengeResponses={
            "USERNAME": params["username"],
            "NEW_PASSWORD": params["newPassword"],
        },
    )
    print(response)
    response = {
        "statusCode": 200,
        "body": json.dumps(response["AuthenticationResult"]),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }

    return response
