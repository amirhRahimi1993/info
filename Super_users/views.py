from django.http import HttpResponse , HttpResponseRedirect
from .models import Dr_info , collector , Hash_capcha
from django.template import loader
import hashlib
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .Generate_capch import Generator
import random
import cv2
#####TEST VIEW #######
from .form import DocumentForm
from django.views.decorators.csrf import csrf_exempt



######################



Expire_Time =300 #set Expire time
username = ""
password = ""


def By_Adder_Doctor_detail(request , collector_id):
    request.session.set_expiry(Expire_Time)

    filters = ""
    try:
        for i in range(len(Dr_info.objects.filter(adder=collector_id))):
            filters = filters + Dr_info.objects.filter(adder=collector_id)[i].Dr_name + " " + Dr_info.objects.filter(adder=collector_id)[i].Dr_family + "<br/>"
    except:
        return HttpResponse("WOW it seems your data dosent avalable")
    return HttpResponse (filters)

def USer_adder(request , collector_id):
    request.session.set_expiry(Expire_Time)
    try:
        X = collector.objects.get(pk=collector_id)
        return HttpResponse(X.name + " " + X.family)
    except:
        return HttpResponse("Collector does not EXIST")

def index(request):
    #g = Generator()
    #g.main()
    return HttpResponse("xxxx")

def Login(request):
    request.session.set_expiry(Expire_Time)
    template = loader.get_template('Super_user/login.html')
    context = {
        'sth':1,
    }
    return HttpResponse(template.render(context , request))
def Super_Usr_Home(request):
    request.session.set_expiry(Expire_Time)
    Email = request.session["username"]
    Password = request.session["password"]
    rand = random.randint(1002,9998)
    Hash_value = Hash_capcha.objects.get(Number=rand).Hash_value
    Num_path = Hash_capcha.objects.get(Number=rand).Number_name
    try:
        collectors = collector.objects.get(Email=Email , password=Password)
    except:
        return HttpResponse("WRONG")
    template = loader.get_template('Super_user/Addinfo.html')
    context ={
        'Email': Email,
        'name': collectors.name,
        'family': collector.family,
        'HASH_VALUE' : Hash_value,
        'img_path' : Num_path
    }
    return HttpResponse(template.render(context, request))
def Report_activity(request):
    request.session.set_expiry(Expire_Time)
    filters = []
    template = loader.get_template("Super_user/Doctor_Template.html")
    collector_id = collector.objects.get(Email=request.session["username"]).id
    filters = Dr_info.objects.filter(adder=collector_id)
    for i in filters:
        i.Dr_name
    context = {
        'filters': filters
    }
    return HttpResponse(template.render(context , request))
def AdvanceSearch(request):
    request.session.set_expiry(Expire_Time)
    filters = []
    template = loader.get_template("Super_user/AdvanceSearch.html")
    collector_id = collector.objects.get(Email=request.session["username"]).id
    filters = Dr_info.objects.filter(adder=collector_id)
    context = {
        'filters': filters
    }
    return HttpResponse(template.render(context , request))
def result(request):
    request.session.set_expiry(Expire_Time)
    template = loader.get_template("Super_user/result.html")
    search_items = []
    item = []
    if request.method == "POST":

        adder_email = request.session["username"]
        Emails =[]

        item.extend(["Dr_name", request.POST["txt_name"]]) if request.POST["txt_name"] != "" else item
        item.extend(["Dr_family", request.POST["txt_family"]]) if request.POST["txt_family"] != "" else item

        item.extend(["Dr_specialty", request.POST["txt_specialty"]]) if request.POST["txt_specialty"] != "" else item
        item.extend(["Dr_telephone", request.POST["txt_tel"]]) if request.POST["txt_tel"] != "" else item

        item.extend(["Dr_mobile", request.POST["txt_mobile"]]) if request.POST["txt_mobile"] != "" else item

        item.extend(["Dr_google_map_link", request.POST["txt_gmap"]]) if request.POST["txt_gmap"] != "" else item
        item.extend(["Dr_Address", request.POST["txt_Address"]]) if request.POST["txt_Address"] != "" else item

        Search_Query = {}
        for i in range(0,len(item)-1,2):
            if not item[i+1] == "":
                Search_Query[item[i]] = item[i+1]
                i= i+1
        dr = Dr_info.objects.filter(**Search_Query)
        if len(dr) != 0 :
            context = {
                'filters' : dr,
                'empty' : 'False',
                'viewer_email' : adder_email,
            }
        else:
            context = {
                'filters': 'متاسفانه درخواست شما نتیجه ای در بر نداشت',
                'empty' : 'True'
            }
    return  HttpResponse(template.render(context,request))


def Logout(request):
    request.session.flush()
    template = loader.get_template("Super_user/Logout.html")
    context = {}
    return HttpResponse(template.render(context,request))

######TEST########
def BasicUploadView(request):
    request.session.set_expiry(Expire_Time)
    template = loader.get_template('Super_user/Test.html')
    context = {
        'sth':1,
    }
    return HttpResponse(template.render(context , request))
def BasicUploadView_ajax(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        data = {
            'path': uploaded_file_url
        }
    return JsonResponse(data)


###########Ajax#################################
def validate_username(request):
    request.session.set_expiry(Expire_Time)
    password = request.GET.get('password', None)
    username = request.GET.get('username', None)
    try:
        if collector.objects.get(Email=username).password == password:
            template = loader.get_template('Super_user/Addinfo.html')
            request.session["username"] = username
            request.session["password"] = password
            data = {
                'is_taken': 'Home',
                'is_correct': 'True'
            }
        else:
            data = {
                'is_taken': 'your user name our password is wrong',
                'is_correct': 'False'
            }

    except:
        data = {
            'is_taken': 'Ur user name our password is wrong',
            'is_correct': 'False'
        }
    return JsonResponse(data)

def insert_Dr_By_adder(request):
    request.session.set_expiry(Expire_Time)
    Hash_capch = request.GET.get('Hash_Value' , None)
    number =  request.GET.get('cap_number' , None)
    if Hash_capcha.objects.get(Hash_value=Hash_capcha).Number != number:
        data = {
            'is_taken': 'کد امنیتی اشتباه می باشد لطفا دوباره تلاش کنید',
            'is_correct': 'False'
        }
        return JsonResponse(data)

    name = request.GET.get('name' , None)
    family = request.GET.get('family' , None)
    location = request.GET.get('location' , None)
    address = request.GET.get('address' , None)
    ph_link = request.GET.get('ph_link', None)
    tel = request.GET.get('tel' , None)
    mbl = request.GET.get('mbl' , None)
    spl = request.GET.get('spl' , None)
    adder_email = request.GET.get('adder_email' , None)
    if len(mbl) != 11:
        data = {
            'is_taken': 'شماره موبایل بایستی ۱۱ رقم باشد',
            'is_correct': 'False'
        }
        return JsonResponse(data)
    try:
        tel_phone = int(mbl)
        mobile = int(spl)
    except:
        data = {
            'is_taken': 'شماره بایستی شامل شامل عدد باشد',
            'is_correct': 'False'
        }
        return JsonResponse(data)
    try:
        col = collector.objects.get(Email=adder_email)
        Answer = Dr_info(Dr_name=name , Dr_family=family , Dr_google_map_link= location , Dr_Address=address , Dr_photo_link=ph_link , Dr_telephone=tel , Dr_mobile=mbl, Dr_specialty=spl , adder=col)
        Answer.save()
        data = {
            'is_taken': 'ثبت اطلاعات با موفقیت انجام شد',
            'is_correct': 'True'
        }
    except:
        data = {
            'is_taken': 'خطایی رخ داده',
            'is_correct': 'False'
        }
    return JsonResponse(data)

def Update_dr(request):
    request.session.set_expiry(Expire_Time)
    name = request.GET.get('dr_name', None)
    family = request.GET.get('dr_family', None)
    location = request.GET.get('dr_gmap', None)
    address = request.GET.get('dr_address', None)
    #ph_link = request.GET.get('dr', None)
    tel = request.GET.get('dr_tel', None)
    mbl = request.GET.get('dr_mbl', None)
    spl = request.GET.get('dr_speciality', None)
    adder_email = request.session['username']
    id = request.GET.get('id', None)
    obj = Dr_info.objects.get(id=id)
    try:
        if not obj.adder.Email == request.session["username"]:
            data = {
                'is_taken': 'خطایی رخ داده',
                'is_correct': 'False'
            }
        else :
            obj.Dr_name = name
            obj.Dr_family = family
            obj.Dr_google_map_link = location
            obj.Dr_Address = address
            obj.Dr_telephone = tel
            obj.Dr_mobile = mbl
            obj.Dr_specialty = spl
            number = int(mbl)
            x = int(tel)
            if len(mbl) == 11:
                data = {
                    'is_taken': 'عملیات به روزرسانی با موفقیت انجام شد',
                    'is_correct': 'True'
                }
                obj.save()
            else :
                data = {
                    'is_taken': 'طول شماره تلفن بایستی شامل ۱۱ رقم باشد',
                    'is_correct': 'False'
                }
    except:
        data = {
            'is_taken': 'خطا رخ داده',
            'is_correct': 'False'
        }
    return JsonResponse(data)
##############################################################