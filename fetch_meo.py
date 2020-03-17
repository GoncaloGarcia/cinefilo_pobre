import requests
import psycopg2
import json
import datetime
import io
import boto3
import os
import constants
import logging
logging.basicConfig(level = logging.INFO)


def fetch_and_parse_MEO(url, con, s3, string_io):
    truncate_db(con)
    for channel in constants.channels:
        date_today = datetime.datetime.now()
        date_lastweek = date_today - datetime.timedelta(days=7)
        req_body = {"service": "channelsguide", "channels": [channel], "dateStart": date_lastweek.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "dateEnd": date_today.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "accountID": ""}
        r = requests.post(url=url, json=req_body)
        logging.info(channel)
        for channel in r.json()["d"]["channels"]:
            channelName = channel["name"]
            for program in channel["programs"]:
                progName = program["name"]
                progDate = program["date"] + " " + program["timeIni"]
                write_to_postgres(con, channelName, progDate, progName)

    con.cursor().copy_expert(constants.query_out, string_io)
    
    try:
        s3.Bucket('www.cinefilopobre.com').put_object(Key="out.csv", Body=string_io.getvalue()) 
        logging.info("Upload Successful")
    except FileNotFoundError:
        logging.info("The file was not found")
    except NoCredentialsError:
        logging.info("Credentials not available")

def truncate_db(con):
    con.cursor().execute("TRUNCATE TABLE tv")

def write_to_postgres(con, channelName, progDate, progName):
    try:
        sql = "INSERT INTO tv (title, channel, time) values ('%s', '%s', '%s')" % (
        progName.replace("'", "''"), channelName, progDate)
        con.cursor().execute(sql)
        con.commit()
    except Exception as e:
        logging.info(e)

def lambda_handler(event, context):
    url = "https://www.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getProgramsFromChannels"
    string_io = io.StringIO()
    con = psycopg2.connect(database="cinefilo", user="cinefilo", password="cinefilo",
                           host="cinefilopobre.ckpkwbhif9f0.us-east-1.rds.amazonaws.com", port="5432")
    s3 = boto3.resource("s3")
    fetch_and_parse_MEO(url, con, s3, string_io)
    con.close()

