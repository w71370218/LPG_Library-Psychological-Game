from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
from trips.models import *
from random import randint
from .forms import TestForm, ChoiceForm, TypeForm, PointRecordForm, BooklistForm
from django.contrib import auth
from django.core.serializers import serialize
import requests
from bs4 import BeautifulSoup

def hello_world(request):
# return HttpResponse("Hello World!")
  return render(request, 'hello.html', {
      'current_time': str(datetime.now()),
})

def index(request):
	return render(request, 'index.html')

def app(request):
	test_num = 3
	test_list = Test.objects.all().order_by('?')[:test_num]
	choice_list = Choice.objects.all()
	type_list = Type.objects.all()
	book_list = Booklist.objects.all()
	pointrecored_list = PointRecord.objects.all()

	
	return render(request, 'app.html', {
		'test_list': test_list, 'choice_list': choice_list, 'type_list': type_list, 'book_list': book_list, 'pointrecored_list': pointrecored_list, 'test_num':test_num,
		})

def administration(request):
	question_num = Test.objects.all().count()
	book_num = Booklist.objects.all().count()
	pointrecord_num = PointRecord.objects.all().count()
	return render(request, 'administration.html', {'question_num': question_num, 'book_num':book_num, 'pointrecord_num':pointrecord_num})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/administration/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/administration/')
    else:
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/administration/')

def test_new(request):
	if request.method == "POST":
		form = TestForm(request.POST)
		if form.is_valid():
			test = form.save(commit=False)
			test.save()
			return redirect('administration', pk=test.pk)
	else:
		form = TestForm()
	return render(request, 'test_edit.html', {'form':form})

def test_edit(request, pk):
	test = get_object_or_404(Test, pk=pk)
	if request.method == "POST":
		form = TestForm(request.POST, instance=test)
		if form.is_valid():
			test = form.save(commit=False)
			test.save()
			return redirect('administration', pk=test.pk)
	else:
		form = TestForm(instance=test)
	return render(request, 'test_edit.html', {'form': form})

def process_result_from_client(request):
	book_num = 3
	result = int(request.POST.get('result'))
	book_list = Booklist.objects.filter(typeof=result)
	
	library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=i&searcharg="
	exclude_id_list = list()
	for book in book_list:
		book_library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=i&searcharg="+ str(book.ISBN)
		res_text = requests.get(book_library_url).text
		soup = BeautifulSoup(res_text , 'html.parser')
		find_soup = soup.find_all('td',width="16%")
		available_bool = 0
		if len(find_soup) > 1:
			for i in find_soup:
				if '可外借' in i.text:
					available_bool = 1
					break
		else:
			if '可外借' in find_soup[0].text:
				available_bool = 1
		if available_bool == 0:
			exclude_id_list.append(book.id)
	result_book_list = book_list.exclude(id__in=exclude_id_list).order_by('?')
	if len(result_book_list) >= book_num:
		result_book_list = result_book_list[:book_num]

	serialized_book_list = serialize('json', result_book_list)
	return JsonResponse(serialized_book_list, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json")