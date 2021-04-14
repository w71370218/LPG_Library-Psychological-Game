from django.db import models
from django.conf import settings
from django.utils import timezone

#class File(models.Model):
#	file = models.FileField(blank=True, null=True)

class Test(models.Model):
	question = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.id)+" : "+self.question
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #title = models.CharField(max_length=200)
    #text = models.TextField()
    #created_date = models.DateTimeField(default=timezone.now)
    #published_date = models.DateTimeField(blank=True, null=True)

    #def publish(self):
     #   self.published_date = timezone.now()
      #  self.save()

    #def __str__(self):
    #    return self.title

class Choice(models.Model):
	question = models.ForeignKey(Test, on_delete=models.RESTRICT,blank=True, null=True)
	choice_number = models.IntegerField(blank=True, null=True)
	text = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.question) +" : "+ self.text
	
class Type(models.Model):
	choice = models.ForeignKey(Choice, on_delete=models.RESTRICT,blank=True, null=True)
	text = models.CharField(max_length=100,blank=True, null=True)

	def __str__(self):
		return self.text +" : "+ str(self.choice)

class Booklist(models.Model):
	title = models.TextField(blank=True, null=True)
	author = models.TextField(blank=True, null=True)
	publisher = models.TextField(blank=True, null=True)
	callnumber = models.CharField(max_length=100,blank=True, null=True)
	ISBN = models.IntegerField(blank=True, null=True)
	picturename = models.ImageField(upload_to='bookcover',blank=True, null=True)
	created_date = models.DateTimeField(blank=True, null=True)
	typeof = models.IntegerField(blank=True, null=True)

	def create(self):
		self.created_date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.ISBN)

class PointRecord(models.Model):
	date = models.DateTimeField(blank=True, null=True)
	studentID = models.IntegerField(blank=True, null=True)
	ISBN = models.IntegerField(blank=True, null=True)

	def earn(self):
		self.date = timezone.now()
		self.save()

	def __str__(self):
		return str(self.id)+" : "+str(self.studentID)