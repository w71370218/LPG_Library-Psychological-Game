from django import forms
from .models import Test, Choice, Type


'''
class TestForm(forms.Modelform):
    class Meta:
        model = Test
        fields = ('question')
        labels = {
            'question': '問題',
            'choice_number': '選項號碼',
            'text':'選項文字',
            'category':'請選擇類別',
            'area':'請選擇縣市',
            'location':'地址',
            'phone_number':'電話',
            'tag':'標籤',
        }
'''
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
    student = models.IntegerField()
    ISBN = models.IntegerField()
    mothod = models.CharField(max_length=50)

    def earn(self):
        self.published_date = timezone.now()
        self.save()
'''