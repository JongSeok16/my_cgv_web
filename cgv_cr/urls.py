
from django.urls import path
from cgv_cr import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('get_cgv/', views.get_cgv, name = 'get_cgv'),
    path('get_lotte/', views.get_lotte, name = 'get_lotte')
]

