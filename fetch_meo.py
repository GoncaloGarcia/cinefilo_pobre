import requests
from jq import jq
import psycopg2
import json
import datetime

channels = ["RTP1","RTP2","SIC","TVI","SICN","RTP3","CMTV", "FOXM","AMCHD","AXBHD","EURCHD","VOD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AXNHD, FOXMH","AMCHD","AXBHD","EURCHD","VOD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AXNHD, PANDA","DISNYJ","KSICHD","BIGGS","CART","DISNY","KOMBH","EURS2H","EURHD","SCPHD", "TVC3HD","TVC4HD","CINEHD","HOLHD","FOXMH","AMCHD","AXBHD","EURCHD","VOD","FOXHD", "FLIFEH","FOXCHD","FOXCOH","AXNHD","AXWHD","SYFHD","TVSEHD","NETFLIX","DEST","DISCVHD", "HISTHD","ODISSHD","NGHD","NGWHD","RTPM","QHD","MTVPHD","BLAZE","BLAZEHD","GAMET", "CIHD","CBSR","TLC","SICCHD","E! HD","MYCHD","24KTHD","TRVHD","LUXHD","FTV", "FTVHD","MCHIC","SMAISHD","VH1","MTVLIVE","TRAHD","MCM P","MCMTHD","CLUBHD","AFRO", "TRACETC","MEZZO","MEZHD","CLASSIC","ICOHD","LOUD","RETRO","JUKEBOX","RTPACR","RTPMA", "ARTV","LVTVHD","TOROTVHD","CAÇAPHD","CAÇAVHD","ELEV4HD","ELEV5HD","ELEV6HD","C180","KURIAKO", "CNOVA","TVVERHD","UME","DOGTV HD","DOGTV","PFC","GNOWHD","REC HD","RECNEW","EURN", "RTPA","TPA","TCV","CNN","BLOOM","FNEWS","SKYN","BBC E","FR24I","I24I", "NHK","CGTNHD","CGTNDHD","EURNIHD","DW-TV","ALJAZHD","RUSST","1RUSS","TVEI","TVE24", "TVGAL","G VIS","CUBAV","A3INTER","A3SERIE","A3CINE","SOMOS","SOLMUSI","CCOCINA","DECASA", "TV5HD","BFM","BFMB","I24F","FR24F","FR2HD","FR3HD","FR5HD","ARTEHD","RAI1", "DWTVA","EURNA","BVN","INTER+","PROTV","BNT4","KBS","IU","CCTV4HD","PHCNE", "RAI2","RAI3","RAINEWS","SCUOLA","STORIA","ZEETV","ZEECIN","SETAS","MAX","PBTVHD", "VENUS","SEXTRM","PENTHS","BODYSEX","HOTHD","VIVID","PLAY","HOT","MCSUHD","SPTV4K", "EURSP","EURS2","KOMBAT","SICK","TVC1","TVC2","TVC3","TVC4","CINE","HOLLW", "FOXM","AMC","AXNBL","EURCH","FOX","FLIFE","FOXCR","FOXCOM","AXN","AXNWH", "SYFY","TVSER","DISCV","HIST","ODISS","NGC","NGWIL","Q","SICR","MTV", "CI","SICC","E!"]


url = "https://www.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getProgramsFromChannels"

con = psycopg2.connect(database = "postgres", user = "postgres", password = "pass", host = "172.17.0.2", port = "5432")

date_today = datetime.datetime.now()
date_lastweek = date_today - datetime.timedelta(days = 7)

print(date_lastweek.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

def fetch_and_parse_MEO():
    for channel in channels:
        req_body = {"service":"channelsguide","channels":[channel],"dateStart":date_lastweek.strftime("%Y-%m-%dT%H:%M:%S.000Z"),"dateEnd":date_today.strftime("%Y-%m-%dT%H:%M:%S.000Z"),"accountID":""}
        r = requests.post(url = url, json = req_body)
        print(channel) 
        try:
            parsed_all = jq('.d.channels[] | .name as $channel | .programs[] | {"name" : .name, "time" : (.date + " " + .timeIni), "channel" : $channel}').transform(r.json(), multiple_output=True)
            for parsed in parsed_all: 
                sql = "INSERT INTO tv (title, channel, time) values ('%s', '%s', '%s')" % (parsed["name"].replace("'", "''"),parsed["channel"], parsed["time"])
                con.cursor().execute(sql)
                con.commit()
        except Exception as e:
            print(e)
fetch_and_parse_MEO()
con.close()
    

