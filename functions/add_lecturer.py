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

    if "lecturer_id" not in params or "email" not in params:
        logger.error("Validation failed. Missing parameters")
        raise Exception("Missing parameters")

    values = (
        params["lecturer_id"],
        params["f_name"],
        params["l_name"],
        params["mobile"],
        params["email"],
        params["gender"],
    )
    print(values)
    sql = "INSERT INTO lecturer_tab (lecturer_id,f_name,l_name,mobile,email,gender) VALUES (%s,%s,%s,%s,%s,%s)"
    print(sql)
    with conn.cursor() as cur:
        cur.execute(
            sql, (values[0], values[1], values[2], values[3], values[4], values[5])
        )
        conn.commit()

    print("user inserted.")

    body = {"message": "Lecturer inserted", "lecturer_id": params["lecturer_id"]}

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