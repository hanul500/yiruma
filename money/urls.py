from django.urls import path
from .views import *

urlpatterns = [
	path('', pay),
    path('<str:y>/<str:m>/', monthlypay),
    path('statistic/', stat_view),
    path('<str:y>/<str:m>/eng/', monthlypay_eng),
    path('<str:y>/<str:m>/<str:stu_id>/', pay_delete),



    
]
