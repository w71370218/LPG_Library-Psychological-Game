from django import forms
from .models import Test, Choice, Type, PointRecord, Booklist, Recommend
from django.db import models
from .validators import validate_file_extension

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.csv'}),validators=[validate_file_extension])

class UploadBooklistFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.csv'}),validators=[validate_file_extension], label='上傳CSV檔')
    image = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*','multiple':'ture'}), label='上傳圖片檔')

class PointRecordForm(forms.ModelForm):
    class Meta:
        model = PointRecord
        fields = ('studentID', 'ISBN','typeof')
        labels = {
            'studentID': '學號',
            'typeof': '類型',
        }

class BooklistForm(forms.ModelForm):
    class Meta:
        model = Booklist
        fields = ('title','author','publisher','callnumber', 'location','ISBN','picturename','typeof')
        labels = {
            'title': '題名',
            'author': '作者',
            'publisher': '出版社',
            'callnumber':'索書號',
            'location': '館藏地',
            'ISBN': 'ISBN',
            'picturename': '封面圖',
            'typeof':'類型'
        }

class RecommendForm(forms.ModelForm):
    class Meta:
        model = Recommend
        fields = ('text','studentID')
        labels = {
            'studentID': '學號',
            'text': '推薦內容',
        }