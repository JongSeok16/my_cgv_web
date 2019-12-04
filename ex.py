from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cgv_web.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from cgv_cr.models import Cgv_data
import time

today_date = time.strftime('%Y%m%d', time.localtime(time.time()))


a = []

def get_cgv () :
    url = 'http://www.cgv.co.kr'
    driver = webdriver.Chrome()
    driver.get('http://www.cgv.co.kr/reserve/show-times/')
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'html.parser')
    soup2 = soup.find('div', id='contents')
    for area in soup2.select('ul > li:nth-child(1) > div.area > ul > li > a ') :
        area_link = url + area.get('href')
        res = requests.get(area_link)
        soup = BeautifulSoup(res.content, "html.parser")
        for i in soup.select("iframe#ifrm_movie_time_table"):
            movie_data_link = url + i.get("src")
            crawling(movie_data_link)
    return a

def crawling (movie_data_link) :

    res = requests.get(movie_data_link)
    soup = BeautifulSoup(res.content, "html.parser")

    for i in soup.select("div.sect-showtimes > ul > li"):
        for ec in i.select("div.type-hall > div.info-timetable > ul > li > a"):
            movie_data = {
                "name" : i.div.a.strong.text.strip(),
                "start_time" : ec.get("data-playstarttime"),
                "end_time" : ec.get("data-playendtime"),
                "area" : ec.get("data-theatername"),
                "seat" : ec.get("data-seatremaincnt"),
                "dt_area" : ec.get("data-screenkorname"),
                "date" : ec.get("data-playymd")
            }
            a.append(movie_data)


# 'name'     : '겨울왕국 2',     'start_time'  : '2130',
# 'end_time' : '2318',          'area'        : '씨네드쉐프 용산아이파크몰',
# 'seat'     : '38',            'dt_area'     : 'CINE de CHEF Salon S관(소파좌석)'

if __name__ == "__main__" :
    get_cgv_data = get_cgv()
    rows = Cgv_data.objects.filter(date=today_date).count()
    # DB에 오늘 날짜의 정보가 없을경우 기존의 데이터 (전 날) 삭제후 새로 (오늘) insert
    if rows == 0 :
        dels = Cgv_data.objects.all()
        dels.delete()
        for i in get_cgv_data :
            cgv_data = Cgv_data(
                name = i["name"] , start_time = i["start_time"],
                end_time = i["end_time"] , area = i["area"],
                seat = i["seat"] , dt_area = i["dt_area"], date = i["date"])
            cgv_data.save()

    # update
    elif rows > 0 :
        for i in get_cgv_data:
            data = Cgv_data.objects.filter(name = i["name"],
                                        start_time = i["start_time"],area = i["area"],
                                        dt_area = i["dt_area"],date = i["date"]).exclude(seat = i["seat"])
            data.update(seat =i["seat"])










