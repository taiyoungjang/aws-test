import sys
import logging
import json
import pymysql
import itertools

db_host  = "localhost"
db_port = 30001
username = "user"
password = "1234"
db_name = "log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=db_host, port=db_port, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    sys.exit()

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.zip_longest([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

def lambda_handler(event, context):
    with conn.cursor() as cur:
        cur.execute("select * from table limit 10")
        results = dictfetchall(cur)
        json_results = json.dumps(results)
        return {
            'statusCode': 200,
            'body': json.dumps(json_results, indent=2)
        }

#ret = lambda_handler("","")
#print(ret)
