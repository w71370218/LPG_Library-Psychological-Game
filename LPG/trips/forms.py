from django import forms
from .models import Test, Choice, Type, PointRecord, Booklist
from django.db import models

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('question',)
        labels = {
            'question': '問題',
            'choice_number': '選項號碼',
            #'text':'選項文字',

        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('question','choice_number','text')
        labels = {
            'question': '問題',
            'choice_number': '選項號碼',
            'text':'選項文字',
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('choice','text')
        labels = {
            'choice': '選項',
            'text': '類型',
        }
        help_texts = {
            'text': '注意: 兩項以上格式以", "分隔',
        }

class PointRecordForm(forms.ModelForm):
    class Meta:
        model = PointRecord
        fields = ('studentID', 'ISBN')
        labels = {
            'studentID': '學號',
        }

class BooklistForm(forms.ModelForm):
    class Meta:
        model = Booklist
        fields = ('title','author','publisher','callnumber','ISBN','picturename')
        labels = {
            'title': '題名',
            'author': '作者',
            'publisher': '出版社',
            'callnumber':'索書號',
            'ISBN': 'ISBN',
            'picturename': '封面圖',
        }

'''
class Test(models.Model):
    question = models.TextField()

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

    def earn(self):
        self.published_date = timezone.now()
        self.save()
'''