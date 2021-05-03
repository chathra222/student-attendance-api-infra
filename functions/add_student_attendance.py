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

    values = (
        params["attendance_id"],
        params["student_id"],
        params["attended_time"],
        params["attended"],
        params["class_id"],
    )
    print(values)
    sql = "INSERT INTO stud_attendance_tab (attendance_id,student_id,attended_time,attended,class_id) VALUES (%s,%s,%s,%s,%s)"
    print(sql)
    with conn.cursor() as cur:
        cur.execute(sql, (values[0], values[1], values[2], values[3], values[4]))
        conn.commit()

    print("Marked attendance")

    body = {
        "message": "Marked Attendance",
        "class_id": params["class_id"],
        "student_id": params["student_id"],
        "attended": params["attended"],
    }

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
