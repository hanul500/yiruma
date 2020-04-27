from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.utils import timezone

def passtopay(request):
	return HttpResponseRedirect('/pay/')

def clear_page(request):
	context = {"title": "Welcome to Ondream"}
	return render(request, "clear.html", context)

def inquiry_view(request):
	inq_obj = inquiry.objects.all()
	tea_obj = Schoolteainfo.objects.all()
	sch_obj = Schoolinfo.objects.all()
	if request.method == 'POST':
		if 'inq_save' in request.POST:
			new_inq = inquiry()
			new_inq.inq_sch = request.POST.get("inq_sch")
			new_inq.inq_tea = request.POST.get("inq_tea")
			new_inq.inq_content = request.POST.get("inq_content")
			new_inq.inq_addtime = timezone.now()
			new_inq.save()
			return HttpResponseRedirect('.')

	context = {'inq_obj':inq_obj, 'tea_obj':tea_obj,'sch_obj':sch_obj}
	return render(request, 'inquiry.html', context)

