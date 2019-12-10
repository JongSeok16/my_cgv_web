from django.shortcuts import render
from cgv_cr.models import Cgv_data
from django.http import HttpResponseRedirect
from django.urls import reverse
from itertools import groupby

# Create your views here.

def index (request) :
    return render(request, 'cgv_movie/index.html')

def get_cgv (request) :
    area_data = request.POST.get('area', False)
    qs = Cgv_data.objects.filter(area__contains=area_data)
    a = []
    mv =[]
    for i in qs :
        dic = {'name' : i.name, 'start_time' : i.start_time, 'area' : i.area,
               'seat': i.seat, 'dt_area' : i.dt_area, 'link' : i.link}
        a.append(dic)
    for k, g in groupby(a, lambda e: e['name']):
        c = {k : list(g)}
        mv.append(c)
    movie_list = {"movie_ls": mv}
    return render(request, 'cgv_movie/get_cgv.html', movie_list)







    # area_data = request.POST.get('area', False)
    # qs = Cgv_data.objects.filter(area__contains=area_data).exclude(seat = "마감" or "매진")
    # movie_list = {"movie_ls" : qs}
    # return render(request, 'cgv_movie/get_cgv.html', movie_list)
    # return HttpResponseRedirect(reverse('see_movie'))

# def see_movie (request) :
    # qs = Cgv_data.objects.f
    # movie_list = {"movie_ls" : qs}
    # return render(request, 'cgv_movie/get_cgv.html', movie_list)

