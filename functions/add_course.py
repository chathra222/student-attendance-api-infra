import json
import logging
import os
import pymysql
import boto3

# Set logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

host = "student-attendance-mysql.cluster-caugssaazeeg.us-east-1.rds.amazonaws.com"
user = "root"
password = "EcCQWDX2S8"
database = "alset"

try:
    conn = pymysql.connect(
        host="student-attendance-mysql.cluster-caugssaazeeg.us-east-1.rds.amazonaws.com",
        user="root",
        passwd="EcCQWDX2S8",
        db="alset",
    )
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)


def handler(event, context):
    params = json.loads(event["body"])
    lambda_client = boto3.client("lambda", region_name="us-east-1")

    if "course_id" not in params or "course_name" not in params:
        logger.error("Validation failed. Missing parameters")
        raise Exception("Missing parameters")

    values = (params["course_id"], params["course_name"])
    print(values)
    sql = "INSERT INTO course_tab (course_id,course_name) VALUES (%s,%s)"
    print(sql)
    with conn.cursor() as cur:
        cur.execute(sql, (values[0], values[1]))
        conn.commit()

    print("Course inserted.")

    body = {"message": "Course Created", "coursename": params["course_name"]}

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
