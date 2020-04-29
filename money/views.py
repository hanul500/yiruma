from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect,HttpResponse
from django.db.models import Q
import datetime
from dateutil.relativedelta import *
from .models import *
from student.models import *


# Create your views here.
def pay(request):
	t = datetime.datetime.today()
	y = t.year
	m = t.month
	return HttpResponseRedirect('%s/%s/'%(y,m))

def monthlypay(request,y,m):
	obj, m_obj = get_pays(y,m)
	now_date = datetime.datetime(year=int(y), month=int(m),day=1)
	pre_y = (now_date+relativedelta(months=-1)).year
	pre_m = (now_date+relativedelta(months=-1)).month
	nxt_y = (now_date+relativedelta(months=1)).year
	nxt_m = (now_date+relativedelta(months=1)).month
	if m_obj != None:
		stulist = m_obj.not_stu()
	else:
		stulist = None

	if request.method == 'POST':
		if 'submit_save' in request.POST:
			pay_appnum_txt = request.POST.getlist('pay_appnum_txt[]')
			pay_appnum_teach = request.POST.getlist('pay_appnum_teach[]')
			pay_txtbook = request.POST.getlist('pay_txtbook[]')
			pay_txtpay = request.POST.getlist('pay_txtpay[]')
			pay_teachpay = request.POST.getlist('pay_teachpay[]')
			pay_memo = request.POST.getlist('pay_memo[]')
			if request.POST.get('complete'):
				m_obj.pay_complete = True
			else:
				m_obj.pay_complete = False
			m_obj.save()
			for a,b,c,d,e,f,i in zip(pay_appnum_txt,pay_appnum_teach,pay_txtbook,pay_txtpay,pay_teachpay,pay_memo,obj):
				i.pay_appnum_txt = a
				i.pay_appnum_teach = b
				i.pay_txtbook = c
				i.pay_txtpay = int(d.replace(',',''))
				i.pay_teachpay = int(e.replace(',',''))
				i.pay_memo = f
				i.save()
			return HttpResponseRedirect('.')
		elif 'create_list' in request.POST:
			newpay_obj = Studentpay_monthly()
			newpay_obj.pay_year = y
			newpay_obj.pay_month = m
			newpay_obj.save()
			stu_obj = Studentinfo.objects.all()
			for i in stu_obj:
				new_pay = Studentpay()
				new_pay.pay_monthly = newpay_obj
				new_pay.pay_stu = i
				new_pay.pay_teachpay = i.stu_money
				new_pay.save()
			return HttpResponseRedirect('.')
		elif 'add_stu' in request.POST:
			m_obj.add_pay(Studentinfo.objects.get(stu_id=request.POST.get('stu_add')))
			return HttpResponseRedirect('.')


	context = {'obj':obj,'stulist':stulist,'m_obj':m_obj,'year':y, 'month':m,'pre_y':str(pre_y), 'pre_m':str(pre_m), 'nxt_y':str(nxt_y),'nxt_m':str(nxt_m)}
	return render(request, 'money/monthly.html', context)

def monthlypay_eng(request,y,m):
	obj, m_obj = get_pay_eng(y,m)
	now_date = datetime.datetime(year=int(y), month=int(m),day=1)
	pre_y = (now_date+relativedelta(months=-1)).year
	pre_m = (now_date+relativedelta(months=-1)).month
	nxt_y = (now_date+relativedelta(months=1)).year
	nxt_m = (now_date+relativedelta(months=1)).month
	if m_obj != None:
		stulist = m_obj.not_stu()
		sum_pay,sum_teach,sum_txt = m_obj.cal_eng()
	else:
		stulist = None

	if request.method == 'POST':
		if 'submit_save' in request.POST:
			pay_appnum_txt = request.POST.getlist('pay_appnum_txt[]')
			pay_appnum_teach = request.POST.getlist('pay_appnum_teach[]')
			pay_txtbook = request.POST.getlist('pay_txtbook[]')
			pay_txtpay = request.POST.getlist('pay_txtpay[]')
			pay_teachpay = request.POST.getlist('pay_teachpay[]')
			pay_memo = request.POST.getlist('pay_memo[]')
			if request.POST.get('complete'):
				m_obj.pay_complete = True
			else:
				m_obj.pay_complete = False
			m_obj.save()
			for a,b,c,d,e,f,i in zip(pay_appnum_txt,pay_appnum_teach,pay_txtbook,pay_txtpay,pay_teachpay,pay_memo,obj):
				i.pay_appnum_txt = a
				i.pay_appnum_teach = b
				i.pay_txtbook = c
				i.pay_txtpay = int(d.replace(',',''))
				i.pay_teachpay = int(e.replace(',',''))
				i.pay_memo = f
				i.save()
			return HttpResponseRedirect('.')
		elif 'create_list' in request.POST:
			newpay_obj = Studentpay_monthly()
			newpay_obj.pay_year = y
			newpay_obj.pay_month = m
			newpay_obj.save()
			stu_obj = Studentinfo.objects.all()
			for i in stu_obj:
				new_pay = Studentpay()
				new_pay.pay_monthly = newpay_obj
				new_pay.pay_stu = i
				new_pay.pay_teachpay = i.stu_money
				new_pay.save()
			return HttpResponseRedirect('.')
		elif 'add_stu' in request.POST:
			m_obj.add_pay(Studentinfo.objects.get(stu_id=request.POST.get('stu_add')))
			return HttpResponseRedirect('.')


	context = {'obj':obj,'stulist':stulist,'m_obj':m_obj,'year':y, 'month':m,'pre_y':str(pre_y), 'pre_m':str(pre_m), 'nxt_y':str(nxt_y),'nxt_m':str(nxt_m),'sum_pay':sum_pay,'sum_txt':sum_txt,'sum_teach':sum_teach}
	return render(request, 'money/monthly_eng.html', context)

def stat_view(request):
	tlist = []
	m = []
	y = []
	total = []
	obj = Studentpay_monthly.objects.all().filter(pay_complete=True)
	for i in obj:
		tlist.insert(0,i.cal_total())
		m.insert(0,i.pay_month)
		y.insert(0,i.pay_year)
	if len(tlist)>12:
		tlist=tlist[:12]
		m=m[:12]
		y=y[:12]
	for i in range(len(tlist)):
		total.append((tlist[i]/max(tlist))*100)
	month_count = len(Studentpay_monthly.objects.all().filter(pay_complete=True))
	total_income = 0
	for i in Studentpay_monthly.objects.all().filter(pay_complete=True):
		total_income += i.cal_total()

	context = {'ziped':zip(tlist,total,y,m),'obj':obj,'month_count':month_count,'total_income':total_income}
	return render(request, 'money/statistic.html', context)

def pay_delete(request,y,m,stu_id):
	stu_obj = get_object_or_404(Studentinfo, stu_id = stu_id)
	pay_obj, pay_m_obj = get_pays(y,m)
	pay_obj = pay_obj.filter(pay_stu = stu_obj)
	if request.method == 'POST':
		if 'submit_delete' in request.POST:
			pay_obj.delete()
			pay_obj, pay_m_obj = get_pays(y,m)
			if len(pay_obj) == 0:
				pay_m_obj.delete()
			return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
	context = {'stu_obj':stu_obj,'pay_m_obj':pay_m_obj}
	return render(request, 'money/pay_delete.html', context)