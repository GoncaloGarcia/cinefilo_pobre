

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


channels = ["RTP1","RTP2","SIC","TVI","SICN","RTP3","CMTV", "FOXM","AMCHD","AXBHD","EURCHD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AMCHD","AXBHD","EURCHD","FOXHD","FLIFEH","FOXCHD","FOXCOH","AXNHD","DISNYJ","KSICHD","BIGGS","CART","DISNY","KOMBH","EURS2H","EURHD", "TVCTOPH","TVCEDIH","CINEHD","HOLHD","FOXMH","AMCHD","AXBHD","EURCHD","FOXHD", "FLIFEH","FOXCHD","FOXCOH","AXNHD","AXWHD","SYFHD","TVSEHD","NETFLIX","DEST","DISCVHD", "HISTHD","NGHD","NGWHD","RTPM","QHD","MTVPHD","TLC","SICCHD","MYCHD","24KTHD","TRVHD","LUXHD","FTV", "FTVHD","MCHIC","SMAISHD","TRAHD","RTPACR","RTPMA", "RTPA","TCV","BBC E", "NHK","CGTNHD","CGTNDHD","RUSST","1RUSS","AXNM","AXNMHD", "TVGAL","G VIS","CUBAV","A3INTER","A3SERIE","A3CINE","SOMOS","SOLMUSI","CCOCINA","DECASA", "TV5HD","BFM","BFMB","I24F","FR24F","FR2HD","FR3HD","FR5HD","ARTEHD","RAI1", "DWTVA","EURNA","BVN","PHCNE", "TVCEMOH","TVCACTH","RAINEWS","MAX","PBTVHD","SPTV4K", "EURSP","EURS2","SICK","TVC1","TVC2","TVC3","TVC4","CINE","HOLLW", "FOXM","AMC","AXNBL","EURCH","FOX","FLIFE","FOXCR","FOXCOM","AXN","AXNWH", "SYFY","TVSER","DISCV","HIST","ODISS","NGC","NGWIL","Q","SICR","MTV", "CI","SICC","E!"]



example_json= """
{
  "d": {
    "__type": "Ptsi.Isites.GridTv.CanaisService.GridTV",
    "ExtensionData": {},
    "services": [],
    "channels": [
      {
        "__type": "Ptsi.Isites.GridTv.CanaisService.Channels",
        "ExtensionData": {},
        "id": 20,
        "name": "SPORT.TV1",
        "sigla": "SPTV1",
        "friendlyUrlName": "",
        "url": "https://www.meo.pt/tv/SPTV1",
        "meogo": false,
        "logo": "https://www.meo.pt/PublishingImages/canais/sport-tv1.png",
        "isAdult": false,
        "categories": [
          {
            "ExtensionData": {},
            "id": 2,
            "name": "Desporto"
          }
        ],
        "types": [
          {
            "ExtensionData": {},
            "id": 0,
            "name": "Gravações Automáticas"
          },
          {
            "ExtensionData": {},
            "id": 1,
            "name": "Restart TV"
          }
        ],
        "programs": [
          {
            "ExtensionData": {},
            "date": "15-3-2020",
            "timeIni": "22:50",
            "timeEnd": "00:50",
            "number": 13753664,
            "uniqueId": "16416719",
            "name": "Reds x Bulls - Super Rugby",
            "synopse": null,
            "imageM": null,
            "imageL": null,
            "imageXL": null,
            "recordType": 0,
            "recordingDefinitionID": "00000000-0000-0000-0000-000000000000",
            "recordingProgramID": "00000000-0000-0000-0000-000000000000",
            "seriesID": "1525522194"
          }
        ],
        "moreInfo": {
          "ExtensionData": {},
          "Label": "Saiba mais",
          "Link": "https://www.meo.pt/tv/canais-servicos-tv/premium/sport-tv"
        },
        "programacaoCanal": {
          "ExtensionData": {},
          "Label": null,
          "Link": null
        }
      }
    ],
    "filters": {
      "ExtensionData": {},
      "types": [
        {
          "ExtensionData": {},
          "id": 0,
          "name": "Gravações Automáticas"
        },
        {
          "ExtensionData": {},
          "id": 1,
          "name": "Restart TV"
        }
      ],
      "categories": [
        {
          "ExtensionData": {},
          "id": 2,
          "name": "Desporto"
        }
      ]
    }
  }
}
"""
