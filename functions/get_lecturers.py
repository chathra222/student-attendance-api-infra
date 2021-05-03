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
    lambda_client = boto3.client("lambda", region_name="us-east-1")

    sql = "SELECT * from lecturer_tab"
    print(sql)
    keys_tup = ("lecturer_id", "f_name", "l_name", "mobile", "email", "gender")
    with conn.cursor() as cur:

        cur.execute(sql)

        rows = cur.fetchall()
        lectuerer_list = []
        for row in rows:
            if len(keys_tup) == len(row):
                dic = {keys_tup[i]: row[i] for i, _ in enumerate(row)}
                lectuerer_list.append(dic)

    print(lectuerer_list)

    response = {
        "statusCode": 200,
        "body": json.dumps(lectuerer_list),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
        },
    }

    return response
