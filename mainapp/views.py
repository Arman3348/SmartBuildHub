from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import requests
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def index(request):
    return render(request, 'index.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def about(request):
    return render(request, 'about.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def Services(request):
    return render(request, 'Services.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def projects(request):
    return render(request, 'projects.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        enq = Enquiry(
            name=name,
            contactno=contactno,
            email=email,
            subject=subject,
            message=message
        )
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request, 'Your enquiry has been submitted successfully!😊')
        return redirect('contact')
    return render(request, 'contact.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def signup(request):
    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        if UserLogin.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please try another one.🤦‍♂️')
            return redirect('signup')
        log = LoginInfo(usertype=usertype, username=email, password=password)
        log.save()
        user = UserLogin(
            usertype=usertype,
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            login=log
        )
        user.save()
        messages.success(request, 'You have signed up successfully!😊')
        return redirect('login')
    return render(request, 'signup.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def login(request):
    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            log = UserLogin.objects.get(email=email, password=password, usertype=usertype)
            if log is not None:
                if log.usertype == "homeowner":
                    request.session['homeownerid'] = email
                    messages.success(request, 'You are logged in successfully!😊')
                    return redirect('homeownerdash')
                elif log.usertype == "contractor":
                    request.session['contractorid'] = email
                    messages.success(request, 'You are logged in successfully!😊')
                    return redirect('contractordash')
                else:
                    messages.error(request, 'Invalid user type. Please try again.🤦‍♂️')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid email or password.🤦‍♂️')
                return redirect('login')
        except UserLogin.DoesNotExist:
            messages.error(request, 'Invalid email, password, or user type.🤦‍♂️')
    return render(request, 'login.html')

@cache_control(no_cache = True,must_revalidate=True,no_store=True )
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            ad = LoginInfo.objects.get(username=username, password=password,usertype = "admin")
            if ad is not None:
                request.session['adminid'] = username
                messages.success(request, 'Welcome Admin!😊')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid username or password.🤦‍♂️')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')