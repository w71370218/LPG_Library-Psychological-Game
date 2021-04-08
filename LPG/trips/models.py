from django.db import models
from django.conf import settings
from django.utils import timezone

class Test(models.Model):
	question = models.TextField()
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
	question = models.ForeignKey(Test, on_delete=models.RESTRICT)
	choice_number = models.IntegerField()
	text = models.TextField()
	
class Type(models.Model):
	choice = models.ForeignKey(Choice, on_delete=models.RESTRICT)
	text = models.CharField(max_length=100)

class Booklist(models.Model):
	title = models.TextField()
	author = models.TextField()
	publisher = models.TextField()
	callnumber = models.CharField(max_length=100)
	ISBN = models.IntegerField()
	picturename = models.ImageField()

class PointRecord(models.Model):
	date = models.DateTimeField(blank=True, null=True)
	studentID = models.IntegerField()
	ISBN = models.IntegerField()
	mothod = models.CharField(max_length=50)

	def earn(self):
		self.published_date = timezone.now()
		self.save()