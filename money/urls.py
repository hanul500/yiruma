from django.urls import path
from .views import *

urlpatterns = [
	path('', pay),
    path('<str:y>/<str:m>/', monthlypay),
    path('statistic/', stat_view),



    
]
