from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db.models import Count
from datetime import datetime
from django.utils import timezone
from trips.models import *
from random import randint
from .forms import *
from django.contrib import auth, messages
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
import io
import base64
from PIL import Image

def hello_world(request):
# return HttpResponse("Hello World!")
  return render(request, 'hello.html', {
      'current_time': str(datetime.now()),
})

def test_img(request):
	book = Booklist.objects.all()[1]
	img_url = str(book.picturename)
	aws_access_key_id = settings.AWS_ACCESS_KEY_ID 
	aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
	s3 = boto3.resource('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	obj = s3.Object('fjulpg',img_url)
	file_stream = io.BytesIO()
	obj.download_fileobj(file_stream)
	image_data = file_stream.getvalue()
	return HttpResponse(image_data, content_type="image/png")


def index(request):
	return render(request, 'index.html')

	
def game(request):
	return render(request, 'game.html')

def app(request):
	test_num = 3
	test_list = Test.objects.all().order_by('?')[:test_num]
	choice_list = Choice.objects.all()
	type_list = Type.objects.all()
	book_list = Booklist.objects.all()
	logo_icon = Img.objects.get(description="logo_icon").img.url
	FB_share_Default = Img.objects.get(description="FB_share_Default").img.url
	return render(request, 'app.html', {
		'test_list': test_list, 'choice_list': choice_list, 'type_list': type_list, 'book_list': book_list, 'test_num':test_num, 'logo_icon':logo_icon, "FB_share_Default":FB_share_Default
		})

def administration(request):
	question_num = Test.objects.all().count()
	book_num = Booklist.objects.all().count()
	pointrecord_num = PointRecord.objects.all().count()
	recommend_num = Recommend.objects.all().count()
	pointrecord_c = PointRecord.objects.values('studentID','typeof')
	pointrecord_count = {}

	for i in pointrecord_c:
		if pointrecord_count.get("i[studentID]") == None:
			pointrecord_count[i['studentID']] = 0
		if i['typeof'] == 1:
			pointrecord_count[i['studentID']] += 2
		elif i['typeof'] == 2:
			pointrecord_count[i['studentID']] += 1
		else:
			pointrecord_count[i['studentID']] += 5

	rank = sorted(pointrecord_count.items(), key =lambda x : x[1],reverse=True)
	try:
		pointrecord_1st = rank[0][0]
	except:
		pointrecord_1st = '從缺'
	try:
		pointrecord_2nd = rank[1][0]
	except:
		pointrecord_2nd = '從缺'
	try:	
		pointrecord_3nd = rank[2][0]
	except:
		 pointrecord_3nd = '從缺'
	return render(request, 'administration.html', {'question_num': question_num, 'book_num':book_num, 'pointrecord_num':pointrecord_num, 'recommend_num':recommend_num,'pointrecord_1st':pointrecord_1st,'pointrecord_2nd':pointrecord_2nd,'pointrecord_3nd':pointrecord_3nd})

def booklist(request):
	book_list = Booklist.objects.all()
	
	return render(request, 'booklist.html', {
		'book_list': book_list
		})

def pointrecord_list(request):
	pointrecord_list = PointRecord.objects.all()
	
	return render(request, 'pointrecord_list.html', {
		'pointrecord_list': pointrecord_list
		})

def testlist(request):
	test_list = Test.objects.all()
	choice_list = Choice.objects.all()
	type_list = Type.objects.all()

	return render(request, 'testlist.html', {
		'test_list': test_list, 'choice_list': choice_list, 'type_list': type_list
		})

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

def lucky_draw(request):
	pointrecord_list = PointRecord.objects.all()
	pointrecord_num = pointrecord_list.count()
	return render(request, 'lucky_draw.html', {
		'pointrecord_list':pointrecord_list, 'pointrecord_num': pointrecord_num,
		})

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

def single_new_test(request):
	test_list = Test.objects.all()
	new_test_id = len(test_list)
	new_test_num = new_test_id + 1
	return render(request, 'single_new_test.html', {'new_test_num':new_test_num})

def proccess_single_test(request):
	if request.method == "POST":
		test_list = Test.objects.all()
		choice_list = Choice.objects.all()
		type_list = Type.objects.all()
		question = request.POST.get('form[question]')
		Test.objects.create(question=question)
		choice_num = (len(request.POST)-2)//2
		for i in range(1,choice_num+1):
			choice_text = request.POST.get('form[choice_text'+str(i)+']')
			choice_type = request.POST.get('form[choice_type'+str(i)+']')
			i_test = test_list.filter(question=question)
			i_choice = Choice.objects.create(question=i_test[0], choice_number=i, text=choice_text)
			Type.objects.create(choice=i_choice,text=choice_type)
		return JsonResponse({'message':'新增成功!'}, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json")
	else:
		return render(request, 'single_new_test.html')

def single_new_book(request):
	if request.method == "POST":
		form = BooklistForm(request.POST,request.FILES)
		if form.is_valid():
			book = form.save(commit=False)
			book.created_date = timezone.now()
			book.save()
			return redirect('/booklist/', pk=book.pk)
	else:
		form = BooklistForm()
	return render(request, 'book_edit.html', {'form':form})

def book_edit(request, pk):
	book = get_object_or_404(Booklist, pk=pk)
	if request.method == "POST":
		form = BooklistForm(request.POST, request.FILES, instance=book)
		if form.is_valid():
			book = form.save(commit=False)
			book.created_date = timezone.now()
			book.save()
			return redirect('booklist', pk=book.pk)
	else:
		form = BooklistForm(instance=book)
	return render(request, 'book_edit.html', {'form': form})

def pointrecord_new(request):
	pointrecord_list = PointRecord.objects.all()
	recent_pointrecord_list = pointrecord_list.order_by('-date')[:3]
	if request.method == "POST":
		form = PointRecordForm(request.POST)
		if form.is_valid():
			pointrecord = form.save(commit=False)
			now = datetime.datetime.now()
			if pointrecord.typeof == 1 or pointrecord.typeof == 2:
				
				pointrecord_for_today = pointrecord_list.filter(studentID=pointrecord.studentID, date__year=now.year, date__month=now.month, date__day=now.day)
				if len(pointrecord_for_today) < 3:
					if not pointrecord_list.filter(studentID=pointrecord.studentID , ISBN=pointrecord.ISBN):
						pointrecord.date = timezone.now()
						pointrecord.save()
						messages.success(request, '成功紀錄!')
						return redirect('/pointrecord/new/', pk=pointrecord.pk)

					else:
						messages.error(request, '重複的紀錄無法輸入')
				else:
					messages.error(request, '今天借閱紀錄已達上限')
			elif pointrecord.typeof == 4: # 3:recommend 4:share
				pointrecord_for_stuednt = pointrecord_list.filter(studentID=pointrecord.studentID)
				if len(pointrecord_for_stuednt) == 0:
					pointrecord.date = timezone.now()
					pointrecord.save()
					messages.success(request, '成功紀錄!')
					return redirect('/pointrecord/new/', pk=pointrecord.pk)
				else:
					messages.error(request, '已經分享過了, 紀錄已存在')

	else:
		form = PointRecordForm()
	return render(request, 'pointrecord_edit.html', {'form':form, 'recent_pointrecord_list': recent_pointrecord_list})

def pointrecord_edit(request, pk):
	pointrecord_list = PointRecord.objects.all()
	pointrecord = get_object_or_404(PointRecord, pk=pk)
	if request.method == "POST":
		form = PointRecordForm(request.POST, instance=pointrecord)
		if form.is_valid():
			pointrecord = form.save(commit=False)
			if not pointrecord_list.filter(studentID=pointrecord.studentID , ISBN=pointrecord.ISBN):
				pointrecord.date = timezone.now()
				pointrecord.save()
				messages.success(request, '成功紀錄!')
	else:
		form = PointRecordForm(instance=pointrecord)
	return render(request, 'pointrecord_edit.html', {'form': form,})

def process_result_from_client(request):
	book_num = 3
	result = int(request.POST.get('result'))
	book_list = Booklist.objects.filter(typeof=result)
#processing result of booklist	
	library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=i&searcharg="
	exclude_id_list = set()
	result_book_id = set()
	while len(exclude_id_list) != len(book_list) and len(result_book_id)<3:
		temp_book_list = book_list.exclude(id__in=exclude_id_list).order_by('?')[:(3-len(result_book_id))]
		for book in temp_book_list:
			try:
				book_library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=Y&searcharg="+ str(book.callnumber)
				res_text = requests.get(book_library_url).text
				soup = BeautifulSoup(res_text , 'html.parser')
				find_soup = soup.find_all('td',width="16%")
				available_bool = 0
				print(book.callnumber)
				if len(find_soup) > 1:
					for i in find_soup:
						if '可外借' in i.text:
							available_bool = 1
							result_book_id.add(book.id)
							break
				else:
					if '可外借' in find_soup[0].text:
						available_bool = 1
						result_book_id.add(book.id)
						break
				if available_bool == 0:
					exclude_id_list.add(book.id)
			except:
				book_library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=i&searcharg="+ str(book.ISBN)
				res_text = requests.get(book_library_url).text
				soup = BeautifulSoup(res_text , 'html.parser')
				find_soup = soup.find_all('td',width="16%")
				available_bool = 0
				print(book.callnumber)
				if len(find_soup) > 1:
					for i in find_soup:
						if '可外借' in i.text:
							available_bool = 1
							result_book_id.add(book.id)
							break
				else:
					if '可外借' in find_soup[0].text:
						available_bool = 1
						result_book_id.add(book.id)
						break
				if available_bool == 0:
					exclude_id_list.add(book.id)
			else:
				pass
			

	result_book_list = book_list.filter(id__in=result_book_id)
#old code : because in heroku using this code will be get error that "WORKER TIME OUT", but new code maybe have same bug, in sercurity, keep old code
#	for book in book_list:
#		book_library_url = "https://library.lib.fju.edu.tw:444/search*cht/?searchtype=Y&searcharg="+ str(book.callnumber)
#		res_text = requests.get(book_library_url).text
#		soup = BeautifulSoup(res_text , 'html.parser')
#		find_soup = soup.find_all('td',width="16%")
#		available_bool = 0
#		if len(find_soup) > 1:
#			for i in find_soup:
#				if '可外借' in i.text:
#					available_bool = 1
#					break
#		else:
#			if '可外借' in find_soup[0].text:
#				available_bool = 1
#		if available_bool == 0:
#			exclude_id_list.append(book.id)
#	result_book_list = book_list.exclude(id__in=exclude_id_list).order_by('?')
#	if len(result_book_list) >= book_num:
#		result_book_list = result_book_list[:book_num]

#processing image
	c = 0
	for book in result_book_list:
		if book.share_img == None:
			picture = book.picturename
			print(picture)
			FB_share = Img.objects.get(description="FB_share_Transparent").img

			book_img = Image.open(picture)
			book_img.load()
			width, height= book_img.size

			book_img = book_img.convert('RGB')

			FB_share_temp = Image.open(FB_share)
			reserved_size = (384,384)
			adjust_coordinate = (115,123)

			if width < height:
				if height > reserved_size[1]:
					book_img.thumbnail(reserved_size)
				else:
					book_img = book_img.resize((int(reserved_size[0]/height*width),reserved_size[1]))

				width, height = book_img.size
				FB_share_temp.paste(book_img, (int(adjust_coordinate[0]+((reserved_size[0]-width)/2)), adjust_coordinate[1]))
			else:
				if width > reserved_size[0]:
					book_img.thumbnail(reserved_size)
				else:
					book_img = book_img.resize((reserved_size[0],int(reserved_size[1]/width*height)))
				width, height = book_img.size
				FB_share_temp.paste(book_img, (adjust_coordinate[0],int(adjust_coordinate[1]+((reserved_size[1]-height)/2))))

			# Save share img
			buffer1 = io.BytesIO()
			FB_share_temp.save(fp=buffer1, format='JPEG')
			#return ContentFile(buffer1.getvalue(), 'share_img.jpg')
			img = ContentFile(buffer1.getvalue(), 'share_img.jpg')

			
			#img = process_share_image(picture)
			share_img = ShareImg.objects.create()
			share_img.img = img
			share_img.save()
			result_book_list[c].share_img = share_img
			result_book_list[c].save()
		result_book_list[c].picturename = result_book_list[c].picturename.url
		c += 1

	serialized_book_list = serialize('json', result_book_list)
	if len(result_book_list) == 0:
		serialized_book_list = '[{"message":"對不起 本類的書太熱門了 目前在圖書館中已經借完了"}]'
	return JsonResponse(serialized_book_list, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json")


def upload_test_file(request):
	test_list = Test.objects.all()
	choice_list = Choice.objects.all()
	type_list = Type.objects.all()
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print(request.FILES['file'])
			try:
				df = pd.read_csv(request.FILES['file'])
				data = df.values.tolist()
				for i in data:
					if not test_list.filter(question=i[0]):
						Test.objects.create(question=i[0])
					i_test = test_list.filter(question=i[0])
					i_choice = Choice.objects.create(question=i_test[0], choice_number=i[1], text=i[2])
					Type.objects.create(choice=i_choice,text=i[3])
				return HttpResponseRedirect('/testlist/')
			except:
				messages.error(request, '檔案資料不正確或內部錯誤!')

	else:
		form = UploadFileForm()
	return render(request, 'upload_test_file.html', {'form': form})

def upload_booklist_file(request):
	book_list = Booklist.objects.all()
	if request.method == 'POST':
		form = UploadBooklistFileForm(request.POST, request.FILES)
		if form.is_valid():
			print(request.FILES)
			print(request.FILES['file'])
			for i in request.FILES.getlist('image'):
				print(type(i))
				print(str(i))
			
			df = pd.read_csv(request.FILES['file'])
			data = df.values.tolist()
			for i in data:
				book = Booklist.objects.create(title=i[0],author=i[1],publisher=i[2],callnumber=i[3],location=i[4],ISBN=i[5],created_date=timezone.now(),typeof=i[7])
				for j in request.FILES.getlist('image'):
					if str(i[6]) == str(j):
						book.picturename = j
						book.save()
			messages.info(request, '上傳成功!')
			return HttpResponseRedirect('/booklist/')
	else:
		form = UploadBooklistFileForm()
	return render(request, 'upload_booklist_file.html', {'form': form})

def share_book(request,id):
	book = get_object_or_404(Booklist, id=id)
	img_url = book.share_img.img.url
	#aws_access_key_id = settings.AWS_ACCESS_KEY_ID 
	#aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
	#s3 = boto3.resource('s3', region_name='us-east-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
	#obj = s3.Object('fjulpg',img_url)
	#file_stream = io.BytesIO()
	#obj.download_fileobj(file_stream)
	#img = base64.b64encode(file_stream.getvalue())
	#img = str(img)[2:-1]
	return render(request, 'share_book.html', {'img': img_url})

def recommend_list(request):
	recommend_list = Recommend.objects.all()
	
	return render(request, 'recommend_list.html', {
		'recommend_list': recommend_list
		})

def recommend_new(request,result):
	recommend_list = Recommend.objects.all()
	pointrecord_list = PointRecord.objects.all()
	if request.method == "POST":
		form = RecommendForm(request.POST)
		if form.is_valid():
			recommend = form.save(commit=False)
			recommend.typeof = result
			recommend.date = timezone.now()
			recommend.save()
			
			pointrecord_for_stuedent = pointrecord_list.filter(studentID=recommend.studentID, typeof=3)
			if len(pointrecord_for_stuedent) == 0:
				pointrecord = PointRecord.objects.create(studentID=recommend.studentID, typeof=3)
				pointrecord.date = timezone.now()
				pointrecord.save()
				messages.success(request, '成功提交!您已經獲得一點!')

			else:
				messages.success(request, '成功提交!')
	else:
		form = RecommendForm()
	return render(request, 'recommend.html', {'form':form})
#********
# reserved img  
# size: 384* 384 px
# x: 115
# y: 123
#********
def process_share_image(img):
	# Open img file
	FB_share = Img.objects.get(description="FB_share_Transparent").img
	book_img = Image.open(img)
	book_img = book_img.convert('RGB')
	FB_share_temp = Image.open(FB_share)
	reserved_size = (384,384)
	adjust_coordinate = (115,123)

	# Process share img
	width, height = book_img.size
	if width < height:
		if height > reserved_size[1]:
			book_img = book_img.thumbnail(reserved_size)
		else:
			book_img = book_img.resize((int(reserved_size[0]/height*width),reserved_size[1]))
		width, height = book_img.size
		FB_share_temp.paste(book_img, (int(adjust_coordinate[0]+((reserved_size[0]-width)/2)), adjust_coordinate[1]))
	else:
		if width > reserved_size[0]:
			book_img = book_img.thumbnail(reserved_size)
		else:
			book_img = book_img.resize((reserved_size[0],int(reserved_size[1]/width*height)))
		width, height = book_img.size
		FB_share_temp.paste(book_img, (adjust_coordinate[0],int(adjust_coordinate[1]+((reserved_size[1]-height)/2))))
	


	# Save share img
	buffer1 = io.BytesIO()
	FB_share_temp.save(fp=buffer1, format='JPEG')
	return ContentFile(buffer1.getvalue(), 'share_img.jpg')
	#return HttpResponse(image_data, content_type="image/png")