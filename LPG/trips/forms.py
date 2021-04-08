from django import forms
from .models import Test



#class 

'''
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
    student = models.IntegerField()
    ISBN = models.IntegerField()
    mothod = models.CharField(max_length=50)

    def earn(self):
        self.published_date = timezone.now()
        self.save()
'''