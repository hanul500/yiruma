from django.urls import path
from .views import *

urlpatterns = [
	path('', student_list),
	path('<str:stu_id>/update/',student_update),
	path('<str:stu_id>/delete/',student_delete),

]
