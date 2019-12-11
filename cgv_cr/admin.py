## parsed_data/admin.py
from django.contrib import admin
## models에서 BlogData를 import 해옵니다.
from cgv_cr.models import Cgv_data,Lotte_data


## 아래의 코드를 입력하면 BlogData를 admin 페이지에서 관리할 수 있습니다.
admin.site.register(Cgv_data)
admin.site.register(Lotte_data)