import boto3
import json
import logging
import os
import pymysql
import datetime

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
    sql = "SELECT * from class_tab"
    print(sql)
    keys_tup = (
        "class_id",
        "lecturer_id",
        "date",
        "start_time",
        "end_time",
        "module_id",
    )
    with conn.cursor() as cur:

        cur.execute(sql)

        rows = cur.fetchall()
        course_list = []
        for row in rows:
            if len(keys_tup) == len(row):
                dic = {keys_tup[i]: row[i] for i, _ in enumerate(row)}
                course_list.append(dic)

    print(course_list)

    response = {
        "statusCode": 200,
        "body": json.dumps(course_list, default=dateconverter),
    }

    return response


def dateconverter(o):
    print(type(o))
    if isinstance(o, datetime.date):
        return o.__str__()