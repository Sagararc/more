from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render ,HttpResponse , redirect , HttpResponseRedirect , get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AttendanceModel , UserLogin ,CheckoutModel,OutletModel,SupFormModel
from urllib.request import urlopen
from .forms import AttendanceForm,CheckoutForm,UserForm,OutletForm,SupForm,RegisterUserForm
from datetime import datetime,timedelta
import csv
from django.http import StreamingHttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test

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
    user = request.user.first_name
    checkin_time = request.session.get('checkin_time', None)
    print(user)
    return render(request , 'dashboard.html',{'user' : user,'checkin_time':checkin_time}) 

@login_required
def userManage(request):
    usr = UserLogin.objects.all()
    
    search = request.GET.get('search')
    cities = request.GET.get('citySearch')

    if search:
        usr = usr.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )
    
    paginator = Paginator(usr, 10)  
    page_number = request.GET.get('page')
    usr = paginator.get_page(page_number)
    
    return render(request, 'usermanager.html', {'usr': usr})


@login_required
def register(request):
    
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        
        
        if form.is_valid() :
           form.save()
           first_name = form.cleaned_data['first_name']
           username = form.cleaned_data['username']
           password = form.cleaned_data['password1']
           user = authenticate(request ,first_name=first_name , username = username , password=password)
           login(request , user)
           return redirect('dash')
        else:
            print(form.errors)
    form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})








@login_required
def attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)
        if form.is_valid():
            url = "https://ipinfo.io/json"
            resp = urlopen(url)
            data = json.load(resp)
            lat = data['loc'].split(',')[0]
            long = data['loc'].split(',')[1]
            checkin = datetime.utcnow() + timedelta(hours=5, minutes=30)
            image = request.FILES.get('checkin_image')
            user = request.user.first_name
            username = request.user.username

            form.instance.user = user
            form.instance.username = username
            form.instance.lat = lat
            form.instance.long = long
            form.instance.checkin = checkin
            form.instance.checkin_image = image
            form.save()
            # Store check-in time in the session
            request.session['checkin_time'] = checkin.strftime('%Y-%m-%d %H:%M:%S')
            
            return redirect('dash')
        else:
            print(form.errors)

    # Get check-in time from the session
    checkin_time = request.session.get('checkin_time', None)
    print(checkin_time)
    form = AttendanceForm(initial={'user': request.user.first_name})
    context = {'user': request.user.first_name, 'checkin_time': checkin_time}
    return render(request, 'attendance.html', context)




@login_required    
def checkout(request):
    user = request.user.first_name
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
            print(request.session['checkout_time'] , checkout)
            request.session.flush()
            return redirect("/logout")
        else:
            print(form.errors)

    # Retrieve check-out time from the session
    checkout_time = request.session.get('checkout_time', None)
    
    form = CheckoutForm(initial={'user': request.user.first_name})
    att = CheckoutModel.objects.all().order_by('-id')
    
    paginator = Paginator(att, 10)  
    page_number = request.GET.get('page')
    att = paginator.get_page(page_number)
    
    context = {'user': request.user.first_name, 'checkout_time': checkout_time, 'att' : att}
    return render(request, 'attendance.html', context)

class CombinedData:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.fields = kwargs
    
    def __str__(self):
        return f"{self.model_name}: {self.fields}"

# Create a custom method to retrieve combined information for a given username
def get_combined_data_for_username(username):
    attendance_data = AttendanceModel.objects.filter(username=username)
    checkout_data = CheckoutModel.objects.filter(username=username)
    
    combined_data = []
    
    for attendance in attendance_data:
        combined_data.append(CombinedData('Attendance', **attendance.__dict__))
    
    for checkout in checkout_data:
        combined_data.append(CombinedData('Checkout', **checkout.__dict__))
    
    combined_data.sort(key=lambda x: x.fields.get('checkin') if 'checkin' in x.fields else x.fields.get('checkout'))
    return combined_data

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
            ts = datetime.now()
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
@login_required
def outlet(request):
    
    out = OutletModel.objects.all().order_by('-id')
    search = request.GET.get('search')
    cities = request.GET.get('citySearch')
    usr = UserLogin.objects.all()
    

    if search:
        out = out.filter(
            Q(name__icontains = search)
        )
    elif cities:
        out = out.filter(
            Q(cityReg__id__icontains=cities)
        )
    paginator = Paginator(out, 10)  
    page_number = request.GET.get('page')
    out = paginator.get_page(page_number)
    return render(request , 'outlet.html' , {'out' : out ,  'usr' : usr })

@login_required
def updateOutlet(request , id):
    
    uid = OutletModel.objects.get(pk=id)
    if request.method == 'POST':
        form = OutletForm(request.POST, instance=uid)
        if form.is_valid():
            form.save()
            return redirect('/outlet')
    else:
        form = OutletForm(instance=uid)
    return render(request, 'updateOutlet.html', {'form': form })

@login_required
def outReg(request):
    
    if request.method == 'POST':
        form = OutletForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/outlet')
    else:
        form = OutletForm()
    return render(request , 'outReg.html' , {'form': form })



@login_required
def import_page(request):
    return render(request , 'import.html')

@login_required
def import_data(request):
    if request.method == 'POST' and 'import' in request.FILES:
        csvfile = request.FILES['import']
        decoded_file = csvfile.read().decode('utf-8').splitlines()

        reader = csv.DictReader(decoded_file)
        c= 1
        rows = ""
        error_message = None
        
        
        for row in reader:
            c +=1
            
            username = row['username']
            
            
            
            if UserLogin.objects.filter(username=username).exists():
                error_message = "Mobile already exists." 
                rows = "Error at row : " + str(c)
                
                
           
           
            password = row['password']

                
            if error_message:
                return render(request, 'import.html', {'error_message': error_message , 'rows' : rows}) 
            UserLogin.objects.create(username=username, password=password)
        return redirect('/dash')
    
    return HttpResponse("Invalid request")


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@login_required
def export_data(request):
    data = UserLogin.objects.all()
    model_fields = UserLogin._meta.fields
    excluded_fields = ['password']
    field_names = [field.name for field in model_fields if field.name not in excluded_fields]

    rows = ([getattr(row, field_name) for field_name in field_names] for row in data)
    rows = list(rows)  # Convert generator object to a list

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in [field_names] + rows),  
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response

def raw_export_data(request):
    data = SupFormModel.objects.all()
    model_fields = SupFormModel._meta.fields
    excluded_fields = ['password']
    field_names = [field.name for field in model_fields if field.name not in excluded_fields]

    rows = ([getattr(row, field_name) for field_name in field_names] for row in data)
    rows = list(rows)  # Convert generator object to a list

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in [field_names] + rows),  
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response

@login_required
def attendence1(request):
    att = AttendanceModel.objects.all().order_by('-id')
    chk = CheckoutModel.objects.all()
    paginator = Paginator(att, 10)  
    page_number = request.GET.get('page')
    att = paginator.get_page(page_number)
    
    return render(request , 'att.html' , {'att' : att , 'chk' : chk})

def is_superuser(user):
    return user.is_superuser


def is_active(user):
     return user.is_active



from django.contrib import messages 

@user_passes_test(is_superuser)
def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Using Django's built-in authentication
        user = authenticate(request, username=username, password=password)
        # Checking if the user exists in your UserLogin model
        if user is not None:
            login(request, user)
            return redirect('/user')
       
        return HttpResponse("Wrong credentials. Please try again.")
    else:
        return render(request, 'adminlogin.html')
    

        

    
@login_required
def raw(request):
    data = SupFormModel.objects.all().order_by('-id')
  
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    return render(request , 'raw.html' , {'data' : data })