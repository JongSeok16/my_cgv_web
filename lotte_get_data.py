import json
import requests
import os
import datetime
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cgv_web.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from cgv_cr.models import Lotte_data


url = "http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx?"
now = datetime.datetime.now()
today = str('%s-%s-%s' % ( now.year, now.month, now.day ))
area_list = ["1013","1018","9010","1004","1009",
             "1003","1017","9056","1012","1019",
             "1022","1015","1007","1001","1002",
             "1014","1016","1021","9053","1008",
             "1010","1005","1011"]

def get_lotte_cr () :
    movie_list = []
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
    return movie_list


if __name__ == "__main__" :
    get_lotte_data = get_lotte_cr()
    rows = Lotte_data.objects.filter(date=today).count()
    # DB에 오늘 날짜의 정보가 없을경우 기존의 데이터 (전 날) 삭제 후 새로 (오늘) insert
    if rows == 0 :
        dels = Lotte_data.objects.all()
        dels.delete()
        for i in get_lotte_data :
            lotte_data = Lotte_data(
                name = i["name"] , start_time = i["start_time"],
                area = i["area"], seat = i["seat"] ,
                dt_area = i["dt_area"], date = i["date"]
            )
            lotte_data.save()

    # update
    # DB에 오늘 날짜의 정보가 있을 경우 기존의 데이터와 비교 후
    # 새롭게 받아온 좌석자리로 update
    elif rows > 0 :
        for i in get_lotte_data:
            data = Lotte_data.objects.filter(
                name = i["name"], start_time = i["start_time"],
                area = i["area"], dt_area = i["dt_area"] ,
                date = i["date"]).exclude(seat = i["seat"])
            data.update( seat =i["seat"] )
