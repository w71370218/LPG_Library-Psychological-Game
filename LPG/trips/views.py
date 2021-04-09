from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from trips.models import *
from random import randint
from .forms import TestForm
	
def hello_world(request):
# return HttpResponse("Hello World!")
  return render(request, 'hello.html', {
      'current_time': str(datetime.now()),
})

def index(request):
	return render(request, 'index.html')

def home(request):
	test_num = 3
	test_list = Test.objects.all().order_by('?')[:test_num]
	choice_list = Choice.objects.all()
	type_list = Type.objects.all()
	book_list = Booklist.objects.all()
	pointrecored_list = PointRecord.objects.all()
	return render(request, 'home.html', {
		'test_list': test_list, 'choice_list': choice_list, 'type_list': type_list, 'book_list': book_list, 'pointrecored_list': pointrecored_list, 'test_num':test_num,
		})

def administration(request):
	return render(request, 'administration.html')

def test_new(request):
	form = TestForm
	return render(request, 'test_edit.html', {'form': form})