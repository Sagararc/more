from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render ,HttpResponse , redirect , HttpResponseRedirect , get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CheckoutModel,OutletModel , AttendanceModel
from urllib.request import urlopen
from .forms import AttendanceForm,CheckoutForm,OutletForm,SupForm,RegisterUserForm
from datetime import datetime,timedelta
import csv
from django.http import StreamingHttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
import re

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Using Django's built-in authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dash')
        return HttpResponse("Wrong credentials. Please try again.")
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
        
@login_required    
def dash(request) :
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today_date = now.date()
    user = request.user.first_name
    username = request.user.username
    checkin_times = AttendanceModel.objects.filter(checkin__startswith=str(today_date), username=username).values_list('checkin', flat=True)
    checkin_time = checkin_times.first() if checkin_times else None
    print(user)
    return render(request , 'dashboard.html',{'user' : user,'checkin_time':checkin_time}) 

@login_required 
def attendance(request):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today_date = now.date()
    username = request.user.username
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)
        attendance_records_today = AttendanceModel.objects.filter(checkin__startswith=str(today_date), username=username)
      
        if attendance_records_today:
            error_message = "Already Checked In For Today"
            return render(request, 'attendance.html', {'error_message' : error_message})

        if form.is_valid():
            checkin = datetime.utcnow() + timedelta(hours=5, minutes=30)
            image = request.FILES.get('checkin_image')
            user = request.user.first_name
            flag = 1
            # lat = request.POST.get('lat')
            # long = request.POST.get('long')
            # print("yes")
            # print("lat : " + lat +"long : "+ long)

            form.instance.user = user
            form.instance.username = username
            form.instance.checkin = checkin
            form.instance.checkin_image = image
            form.instance.flag = flag

            # Get the user's location
            url = "https://ipinfo.io/json"
            resp = urlopen(url)
            data = json.load(resp)
            lat = data['loc'].split(',')[0]
            long = data['loc'].split(',')[1]

            form.instance.lat = lat
            form.instance.long = long
            
            form.save()
            request.session['checkin_time'] = checkin.strftime('%Y-%m-%d %H:%M:%S')

            # Remove check-in time from the session
            request.session.pop('checkin_time', None)
            
            return redirect('dash')
        else:
            print(form.errors)

    checkin_times = AttendanceModel.objects.filter(checkin__startswith=str(today_date), username=username).values_list('checkin', flat=True)
    checkin_time = checkin_times.first() if checkin_times else None
    print("checkin" , checkin_time)
    form = AttendanceForm(initial={'user': request.user.first_name})
    context = {'user': request.user.first_name, 'checkin_time': checkin_time}
    return render(request, 'attendance.html', context)




@login_required    
def checkout(request):
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    today_date = now.date()
    user = request.user.first_name
    username = request.user.username

    # Check if the user has already checked out for today
    checkout_records_today = CheckoutModel.objects.filter(checkout__startswith=str(today_date), username=username)
    print(checkout_records_today)
    if checkout_records_today:
        error_message = "Already Checked Out For Today"
        return render(request, 'attendance.html', {'error_message': error_message})

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            url = "https://ipinfo.io/json"
            resp = urlopen(url)
            data = json.load(resp)
            lat = data['loc'].split(',')[0]
            long = data['loc'].split(',')[1]
            checkout = datetime.utcnow() + timedelta(hours=5, minutes=30)
            image = request.FILES.get('checkout_image')
            username = request.user.username
            
            # Assign form data before saving
            form.instance.user = user
            form.instance.username = username
            form.instance.lat = lat
            form.instance.long = long
            form.instance.checkout = checkout
            form.instance.checkout_image = image
            form.save()

            # Store check-out time in the session
            request.session['checkout_time'] = checkout.strftime('%Y-%m-%d %H:%M:%S')
            
            # You have this line, but it immediately removes the value from the session, so it won't be available for printing.
            # Consider removing this line or using it where needed.
            request.session.pop('checkout_time', None)
            
            return redirect('logout')  # Assuming you have a 'logout' URL pattern defined
        else:
            print(form.errors)

    checkout_times = CheckoutModel.objects.filter(checkout__startswith=str(today_date), username=username).values_list('checkout', flat=True)
    checkout_time = checkout_times.first() if checkout_times else None
    print(checkout)
    print(checkout_time)  # This should print checkout_time even if it's None or there's an error

    form = CheckoutForm(initial={'user': user})
    att = CheckoutModel.objects.all().order_by('-id')
    
    paginator = Paginator(att, 10)  
    page_number = request.GET.get('page')
    att = paginator.get_page(page_number)
    
    context = {'user': user, 'checkout_time': checkout_time, 'att' : att}
    return render(request, 'attendance.html', context)






@login_required
def supForm(request):
    user = request.user.first_name
    username = request.user.username
    print(user)
    
    out = OutletModel.objects.all()
    if request.method == "POST":
        form = SupForm(request.POST)
        if form.is_valid():
            url = "https://ipinfo.io/json"
            resp = urlopen(url)
            data = json.load(resp)
            user = request.user.first_name
            username = request.user.username
            outlet = request.POST.get('outlet')
            uniform = request.POST.getlist('uniform')
            grooming = request.POST.getlist('grooming')
            ol = request.POST.get('ol')
            po = request.POST.get('po')
            sfm = request.POST.get('sfm')
            sapp = request.POST.get('sapp')
            leaf = request.POST.get('leaf')
            dapp = request.POST.get('dapp')
            script = request.POST.get('script')
            confi = request.POST.get('confi')
            calls = request.POST.get('calls')
            ps = request.POST.get('ps')
            lat = data['loc'].split(',')[0]
            long = data['loc'].split(',')[1]
            ts = datetime.utcnow() + timedelta(hours=5, minutes=30)
            outlet_id = request.POST.get('outlet')  
            outlet_instance = OutletModel.objects.get(pk=outlet_id)
            print(outlet_instance)
            
            form.instance.user = user
            form.instance.username = username
            form.instance.outlet = outlet_instance
            form.instance.uniform = ', '.join(uniform) if uniform else ''
            form.instance.grooming = ', '.join(grooming) if grooming else ''
            form.instance.ol = ol
            form.instance.po = po
            form.instance.sfm = sfm
            form.instance.sapp = sapp
            form.instance.leaf = leaf
            form.instance.dapp = dapp
            form.instance.script = script
            form.instance.confi = confi
            form.instance.calls = calls
            form.instance.ps = ps
            form.instance.lat = lat
            form.instance.long = long
            form.instance.ts = ts
            form.save()
            return redirect('/success')
        else:
            print(form.errors)   
    return render(request , 'supForm.html' , {'user' : user , 'out' : out})


@login_required
def success(request):
    return render(request , 'success.html')

