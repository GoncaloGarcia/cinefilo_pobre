import requests
import psycopg2
import json
import datetime
import io
import boto3
import os

channels = ["RTP1","RTP2","SIC","TVI","SICN","RTP3","CMTV", "FOXM","AMCHD","AXBHD","EURCHD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AMCHD","AXBHD","EURCHD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AXNHD","DISNYJ","KSICHD","BIGGS","CART","DISNY","KOMBH","EURS2H","EURHD", "TVCTOPH","TVCEDIH","CINEHD","HOLHD","FOXMH","AMCHD","AXBHD","EURCHD","FOXHD", "FLIFEH","FOXCHD","FOXCOH","AXNHD","AXWHD","SYFHD","TVSEHD","NETFLIX","DEST","DISCVHD", "HISTHD","NGHD","NGWHD","RTPM","QHD","MTVPHD","TLC","SICCHD","MYCHD","24KTHD","TRVHD","LUXHD","FTV", "FTVHD","MCHIC","SMAISHD","TRAHD","RTPACR","RTPMA", "RTPA","TCV","BBC E", "NHK","CGTNHD","CGTNDHD","RUSST","1RUSS","AXNM","AXNMHD", "TVGAL","G VIS","CUBAV","A3INTER","A3SERIE","A3CINE","SOMOS","SOLMUSI","CCOCINA","DECASA", "TV5HD","BFM","BFMB","I24F","FR24F","FR2HD","FR3HD","FR5HD","ARTEHD","RAI1", "DWTVA","EURNA","BVN","PHCNE", "TVCEMOH","TVCACTH","RAINEWS","MAX","PBTVHD","SPTV4K", "EURSP","EURS2","SICK","TVC1","TVC2","TVC3","TVC4","CINE","HOLLW", "FOXM","AMC","AXNBL","EURCH","FOX","FLIFE","FOXCR","FOXCOM","AXN","AXNWH", "SYFY","TVSER","DISCV","HIST","ODISS","NGC","NGWIL","Q","SICR","MTV", "CI","SICC","E!"]


query_out = """
copy ( select  
	title,
	array_to_string(ratings, '-'),
	channels,
	array_to_string(array_agg(time order by time), E'<br>')
	
from 
	(select tv.title,
		array_agg(distinct ( movie_ratings.rating , titleid )) as ratings,
		array_to_string(array_agg(distinct tv.channel), E'<br>') as channels,
		time
	from tv, movie_ratings 
	where tv.title = movie_ratings.title 
	group by tv.title, time
	order by ratings desc) as prev
group by title, channels, ratings
order by ratings desc) to stdout with delimiter '\t'
"""

def fetch_and_parse_MEO(url, con):
    con.cursor().execute("TRUNCATE TABLE tv")
    for channel in channels:
        date_today = datetime.datetime.now()
        date_lastweek = date_today - datetime.timedelta(days=7)
        print(date_lastweek.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
        req_body = {"service": "channelsguide", "channels": [channel], "dateStart": date_lastweek.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "dateEnd": date_today.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "accountID": ""}
        r = requests.post(url=url, json=req_body)
        print(channel)
        for channel in r.json()["d"]["channels"]:
            channelName = channel["name"]
            for program in channel["programs"]:
                progName = program["name"]
                progDate = program["date"] + " " + program["timeIni"]
                try:
                    sql = "INSERT INTO tv (title, channel, time) values ('%s', '%s', '%s')" % (
                        progName.replace("'", "''"), channelName, progDate)
                    con.cursor().execute(sql)
                    con.commit()
                except Exception as e:
                    print(e)

    f = io.StringIO()
    con.cursor().copy_expert(query_out, f)



    s3 = boto3.resource("s3")
    print(s3)
    try:
        s3.Bucket('www.cinefilopobre.com').put_object(Key="out.csv", Body=f.getvalue()) 
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")


def lambda_handler(event, context):
    url = "https://www.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getProgramsFromChannels"
    con = psycopg2.connect(database="cinefilo", user="cinefilo", password="cinefilo",
                           host="cinefilopobre.ckpkwbhif9f0.us-east-1.rds.amazonaws.com", port="5432")
    fetch_and_parse_MEO(url, con)
    con.close()

