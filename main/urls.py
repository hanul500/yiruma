from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',passtopay),
    path('pay/',include('money.urls')),
    path('student/',include('student.urls')),
]
