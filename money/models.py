from django.db import models
from student.models import *
from django.db.models import Q

class Studentpay_monthly(models.Model):
	def __str__(self):
		return str(self.pay_year) + '년 ' + str(self.pay_month) + '월'
	pay_year = models.CharField(blank=True,null=True,max_length=120)
	pay_month = models.CharField(blank=True,null=True,max_length=120)
	pay_complete = models.BooleanField(default=False)
	def cal_total(self):
		sum_pay = 0
		obj = Studentpay.objects.all().filter(pay_monthly=self)
		for i in obj:
			sum_pay += i.pay_txtpay
			sum_pay += i.pay_teachpay
		return sum_pay
	def cal_pur(self):
		sum_pay = 0
		obj = Studentpay.objects.all().filter(Q(pay_monthly=self)&Q(pay_stu__stu_category="푸르넷"))
		for i in obj:
			sum_pay += i.pay_txtpay
			sum_pay += i.pay_teachpay
		return sum_pay
	def cal_yiru(self):
		sum_pay = 0
		obj = Studentpay.objects.all().filter(Q(pay_monthly=self)&Q(pay_stu__stu_category="이루마"))
		for i in obj:
			sum_pay += i.pay_txtpay
			sum_pay += i.pay_teachpay
		return sum_pay
	def not_stu(self):
		stu_obj = Studentinfo.objects.all()
		not_stu_obj = []
		for i in stu_obj:
			if len(Studentpay.objects.all().filter(Q(pay_monthly=self)&Q(pay_stu=i)))==0:
				not_stu_obj.append(i)
		return not_stu_obj

	def add_pay(self, stu_obj):
		new_pay = Studentpay()
		new_pay.pay_monthly = self
		new_pay.pay_stu = stu_obj
		new_pay.pay_teachpay = stu_obj.stu_money
		new_pay.save()
		return new_pay


class Studentpay(models.Model):
	def __str__(self):
		return str(self.pay_monthly.pay_year) + '년 ' + str(self.pay_monthly.pay_month) + '월 ' + str(self.pay_stu.stu_name)
	pay_monthly = models.ForeignKey(Studentpay_monthly, on_delete=models.CASCADE)
	pay_stu = models.ForeignKey(Studentinfo, on_delete=models.CASCADE)
	pay_appnum_teach = models.CharField(blank=True,null=True,max_length=120)
	pay_appnum_txt = models.CharField(blank=True,null=True,max_length=120)
	pay_txtbook = models.CharField(blank=True,null=True,max_length=120)
	pay_txtpay = models.IntegerField(blank=True,null=True, default=0)
	pay_teachpay = models.IntegerField(blank=True,null=True,default=0)
	pay_memo = models.TextField(blank=True,null=True)

def get_pays(y,m):
	obj = Studentpay_monthly.objects.all().filter(Q(pay_year=y)&Q(pay_month=m))
	if len(obj) == 0:
		return None, None
	else:
		return Studentpay.objects.all().filter(pay_monthly=obj[0]) , obj[0]

