import boto3
import json
import logging
import os


# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


poolId="us-east-1_wYIgs9wnk"
clientId="3rbb9pn62nncdbc0q19akncars"
def handler(event, context):
    params = json.loads(event['body'])
    congito_client = boto3.client('cognito-idp', region_name="us-east-1")
   response = congito_client.change_password(
    PreviousPassword=params['oldpw'],
    ProposedPassword=params['newpw'],
    AccessToken=params['accesstoken']
    )
    print(response)
    body = {"message": username+" User Signed In",
                   "username": params['username']}           
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

