import requests
import json
from datetime import datetime
import pprint
url = "http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx?"
now = datetime.now()
today = str('%s-%s-%s' % ( now.year, now.month, now.day ))
movie_list = []
area_list = ["1013","1018","9010","1004","1009",
             "1003","1017","9056","1012","1019",
             "1022","1015","1007","1001","1002",
             "1014","1016","1021","9053","1008",
             "1010","1005","1011"]

for area_code in area_list :

    dic = {
        "MethodName":"GetPlaySequence",
        "channelType":"HO",
        "osType":"Chrome",
        "osVersion":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "playDate": today,
        "cinemaID":"1|1|" + area_code ,
        "representationMovieCode":""}

    # 위의 dic 변수의 내용을 paramList 라는 변수명으로 다시 설정합니다.
    # encode() 를 하지 않으면 해당 페이지를 접속했을경우 인코딩 오류가 발생합니다.
    data = {"paramList": str(dic).encode()}

    # 해당 주소로 paramList 변수의 데이터를 POST 형태로 전송합니다.
    # for i in area_list :
    r = requests.post(url, data=data)

    result = json.loads(r.text)

    for i in result['PlaySeqs']['Items']:
        if i.get('IsBookingYN') == 'N':
            i['BookingSeatCount'] = '마감'
        movie_dic = {
            "name": i.get('MovieNameKR'), "dt_area": i.get('ScreenNameKR'),
            "start_time": i.get('StartTime'), "seat": i.get('BookingSeatCount'),
            "area": i.get('CinemaNameKR'), "date": today
        }
        movie_list.append(movie_dic)
pprint.pprint(movie_list)
