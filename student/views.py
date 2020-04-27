from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect,HttpResponse
from django.db.models import Q
import datetime
from dateutil.relativedelta import *
from .models import *


# Create your views here.
def student_list(request):
	stu_obj = Studentinfo.objects.all()
	if request.method == 'POST':
		if 'submit_new' in request.POST:
			new_stu = Studentinfo()
			new_stu.stu_name = request.POST.get('stu_name')
			new_stu.stu_category = request.POST.get('stu_category')
			new_stu.stu_num = request.POST.get('stu_num')
			new_stu.stu_card = request.POST.get('stu_card')
			new_stu.stu_cardbank = request.POST.get('stu_cardbank')
			new_stu.stu_validdate = request.POST.get('stu_validdate')
			new_stu.stu_subj = request.POST.get('stu_subj')
			new_stu.stu_money = int(request.POST.get('stu_money').replace(',',''))
			new_stu.make_id()
			new_stu.save()
			return HttpResponseRedirect('.')
	context = {'stu_obj':stu_obj}
	return render(request, 'student/student.html', context)

def student_update(request, stu_id):
	stu_obj = get_object_or_404(Studentinfo, stu_id = stu_id)
	if request.method == 'POST':
		if 'submit_update' in request.POST:
			stu_obj.stu_name = request.POST.get('stu_name')
			stu_obj.stu_category = request.POST.get('stu_category')
			stu_obj.stu_num = request.POST.get('stu_num')
			stu_obj.stu_card = request.POST.get('stu_card')
			stu_obj.stu_cardbank = request.POST.get('stu_cardbank')
			stu_obj.stu_validdate = request.POST.get('stu_validdate')
			stu_obj.stu_subj = request.POST.get('stu_subj')
			stu_obj.stu_money = int(request.POST.get('stu_money').replace(',',''))
			stu_obj.save()
			return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
	context = {'stu_obj':stu_obj}
	return render(request, 'student/student_update.html', context)

def student_delete(request, stu_id):
	stu_obj = get_object_or_404(Studentinfo, stu_id = stu_id)
	if request.method == 'POST':
		if 'submit_delete' in request.POST:
			stu_obj.delete()
			return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
	context = {'stu_obj':stu_obj}
	return render(request, 'student/student_delete.html', context)