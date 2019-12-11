from django.db import models

# Create your models here.

class Cgv_data (models.Model) :
    name = models.CharField(max_length=50,null=True)
    start_time = models.CharField(max_length=50,null=True)
    area = models.CharField(max_length=50,null=True)
    seat = models.CharField(max_length=50,null=True)
    dt_area = models.CharField(max_length=50,null=True)
    date = models.CharField(max_length=50,null=True)
    link = models.URLField(null=True)

    def __str__(self):
    	return self.area

class Lotte_data (models.Model) :
    name = models.CharField(max_length=50,null=True)
    start_time = models.CharField(max_length=50,null=True)
    area = models.CharField(max_length=50,null=True)
    seat = models.CharField(max_length=50,null=True)
    dt_area = models.CharField(max_length=50,null=True)
    date = models.CharField(max_length=50,null=True)

    def __str__(self):
    	return self.area
