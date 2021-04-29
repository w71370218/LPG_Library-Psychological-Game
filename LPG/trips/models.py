from django.db import models
from django.conf import settings
from django.utils import timezone

#class File(models.Model):
#	file = models.FileField(blank=True, null=True)

class ShareImg(models.Model):
	img = models.ImageField(upload_to='share_img',blank=True, null=True, verbose_name='圖片')

class Icon(models.Model):
	icon =  models.ImageField(upload_to='icon',blank=True, null=True, verbose_name='圖片')
	description = models.CharField(max_length=100,blank=True, null=True, verbose_name='描述')

class Test(models.Model):
	question = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.id)+" : "+self.question

class Choice(models.Model):
	question = models.ForeignKey(Test, on_delete=models.RESTRICT,blank=True, null=True, verbose_name='問題')
	choice_number = models.IntegerField(blank=True, null=True, verbose_name='選項編號')
	text = models.TextField(blank=True, null=True, verbose_name='選項文字')

	def __str__(self):
		return str(self.question) +" : "+ self.text
	
class Type(models.Model):
	choice = models.ForeignKey(Choice, on_delete=models.RESTRICT,blank=True, null=True, verbose_name='屬於的選項')
	text = models.CharField(max_length=100,blank=True, null=True, verbose_name='類型')

	def __str__(self):
		return self.text +" : "+ str(self.choice)

class Booklist(models.Model):
	title = models.TextField(blank=True, null=True, verbose_name='題名')
	author = models.TextField(blank=True, null=True, verbose_name='作者')
	publisher = models.TextField(blank=True, null=True, verbose_name='出版者')
	callnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name='索書號')
	location = models.CharField(max_length=100,blank=True, null=True, verbose_name='館藏地')
	ISBN = models.CharField(max_length=13,blank=True, null=True, verbose_name='ISBN')
	picturename = models.ImageField(upload_to='bookcover',blank=True, null=True, verbose_name='圖片')
	created_date = models.DateTimeField(blank=True, null=True, verbose_name='創建時間')
	typeof = models.IntegerField(blank=True, null=True, verbose_name='類型')
	share_img = models.ForeignKey(ShareImg, on_delete=models.RESTRICT,blank=True, null=True, verbose_name='分享預覽圖')

	def create(self):
		self.created_date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.ISBN)

class PointRecord(models.Model):
	date = models.DateTimeField(blank=True, null=True, verbose_name='日期')
	studentID = models.IntegerField(blank=True, null=True, verbose_name='學號')
	ISBN = models.CharField(max_length=13,blank=True, null=True, verbose_name='ISBN')

	def earn(self):
		self.date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.id)+" : "+str(self.studentID)