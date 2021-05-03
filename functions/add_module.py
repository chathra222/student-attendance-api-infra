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
except Exception as e:
    print(e)


def handler(event, context):
    params = json.loads(event["body"])

    if "module_id" not in params or "lecturer_id" not in params:
        logger.error("Validation failed. Missing parameters")
        raise Exception("Missing parameters")

    values = (
        params["module_id"],
        params["name"],
        params["lecturer_id"],
        params["course_id"],
    )
    print(values)
    moduletabsql = (
        "INSERT INTO module_tab (module_id,name,lecturer_id) VALUES (%s,%s,%s)"
    )
    coursemoduletabsql = (
        "INSERT INTO course_module_tab (course_id,module_id) VALUES (%s,%s)"
    )
    print(moduletabsql)
    with conn.cursor() as cur:
        cur.execute(moduletabsql, (values[0], values[1], values[2]))
        cur.execute(coursemoduletabsql, (values[3], values[0]))
        conn.commit()

    print("Module inserted.")

    body = {"message": "Module Created", "module_id": params["module_id"]}

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


# if user is student,upload source image to the pool and save the bucket name and key in the database
