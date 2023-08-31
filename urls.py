from django.urls import path 
from django.contrib.auth.views import LoginView
from .views import login_view,dash,attendance,raw_export_data,success,attendence1,raw,outReg,supForm,outlet,updateOutlet,adminLogin,checkout,export_data,import_data,import_page,register,logout_user,userManage
urlpatterns = [
    path('' , LoginView.as_view(template_name='login.html') , name='login'),
    path('logout/' , logout_user, name= 'logout'),
    path('dash/' , dash , name='dash'),
    path('attendance/' , attendance , name='attendance'),
    path('checkout/' , checkout , name='checkout'),
    path('export/', export_data, name='export_data'),
    path('export1/', raw_export_data, name='raw_export_data'),
    path('import_page/', import_page, name='import_page'),
    path('import/', import_data, name='import_data'),
    path('register/' , register , name = 'register'),
    path('user/' , userManage , name = 'user'),
    path('attendence1/' , attendence1, name = 'attendence1'),
    path('admin-login/' , adminLogin, name = 'adminLogin'),
    path('outReg/' , outReg, name = 'outReg'),
    path('outlet/' , outlet, name = 'outlet'),
    path('updateOutlet/<int:id>/' , updateOutlet, name = 'updateOutlet'),
    path('form/' , supForm , name='supForm'),
    path('raw/' ,raw , name= 'raw'),
    path('success/' , success , name='success')
   
]
