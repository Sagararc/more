from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render ,HttpResponse , redirect , HttpResponseRedirect , get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from more.models import AttendanceModel , UserLogin ,CheckoutModel,OutletModel,SupFormModel
from urllib.request import urlopen
from more.forms import OutletForm,RegisterUserForm
from datetime import datetime,timedelta
import csv
from django.http import StreamingHttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


def is_superuser(user):
    return user.is_superuser


def is_active(user):
     return user.is_active



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

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/adminLogin')
        


@user_passes_test(is_superuser)
@login_required
def userManage(request):
    usr = User.objects.all()
    
    search = request.GET.get('search')
 

    if search:
        usr = usr.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )
    
    paginator = Paginator(usr, 10)  
    page_number = request.GET.get('page')
    usr = paginator.get_page(page_number)
    
    return render(request, 'usermanager.html', {'usr': usr})

@user_passes_test(is_superuser)
@login_required
def register(request):
    
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        
        
        if form.is_valid() :
           form.save()
        #    first_name = form.cleaned_data['first_name']
        #    username = form.cleaned_data['username']
        #    password = form.cleaned_data['password1']
        #    user = authenticate(request ,first_name=first_name , username = username , password=password)
        
           return redirect('user')
        else:
            print(form.errors)
    form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})













@user_passes_test(is_superuser)
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
@user_passes_test(is_superuser)
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
@user_passes_test(is_superuser)
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

@user_passes_test(is_superuser)
@login_required
def import_page(request):
    return render(request , 'import.html')
@user_passes_test(is_superuser)
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
@user_passes_test(is_superuser)
@login_required
def export_data(request):
    data = User.objects.all()
    model_fields = User._meta.fields
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

@user_passes_test(is_superuser)
@login_required
def raw_export_data(request):
    data = SupFormModel.objects.all()
    model_fields = SupFormModel._meta.fields
    excluded_fields = ['password']
    field_names = [field.name for field in model_fields if field.name not in excluded_fields]

    # Add your custom headers here
    custom_headers = ["Id", "User","Code" ,"Outlet","MO Name", "Uniform" , "Grooming" , "Sharing the Outlet location" , "Sharing the Present Offer information" ,
                   "Sharing the benefits of shopping from MORE","Showing the App", "Handed over the Leaflet" , "Pushed customer for App Download" , "Script delivery" , "How confident she was while interection" , "How Many Calls MO did till supervisor Visit",
                  "Photo Shared with MO on Group" , "Latitude" , "Longitude" , "Time of Visit" , "Remark" ]

    rows = ([getattr(row, field_name) for field_name in field_names] for row in data)
    rows = list(rows)  # Convert generator object to a list

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    # Create a list containing the headers and the rows
    csv_data = [custom_headers]  + rows

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in csv_data),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response
@user_passes_test(is_superuser)
@login_required
def attendence1(request):
    att = AttendanceModel.objects.all().order_by('-id')
    chk = CheckoutModel.objects.all()
    paginator = Paginator(att, 10)  
    page_number = request.GET.get('page')
    att = paginator.get_page(page_number)
    
    return render(request , 'att.html' , {'att' : att , 'chk' : chk})





    


        

@user_passes_test(is_superuser)
@login_required
def raw(request):
    data = SupFormModel.objects.all().order_by('-id')
  
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    return render(request , 'raw.html' , {'data' : data })