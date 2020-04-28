from django.db import models

# Create your models here.
class Studentinfo(models.Model):
	def __str__(self):
		return str(self.stu_name)
	stu_id = models.CharField(blank=True,null=True,max_length=120)
	stu_name = models.CharField(blank=True,null=True,max_length=120)
	stu_num = models.CharField(blank=True,null=True,max_length=120)
	stu_category = models.CharField(blank=True,null=True,max_length=120)
	stu_card = models.CharField(blank=True,null=True,max_length=120)
	stu_cardbank = models.CharField(blank=True,null=True,max_length=120)
	stu_validdate = models.CharField(blank=True,null=True,max_length=120)
	stu_subj = models.CharField(blank=True,null=True,max_length=120)
	stu_money = models.IntegerField(blank=True,null=True)
	class Meta:
		ordering = ['stu_name']
	def make_id(self):
		idlist=[]
		if Studentinfo.objects.last():
			for i in Studentinfo.objects.all():
				idlist.append(i.stu_id[1:])
			self.stu_id = "S"+ "%04d"%(int(max(idlist))+1)
		else:
			self.stu_id = "S0000"
