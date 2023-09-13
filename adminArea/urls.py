from django.urls import path 

from . import views 
urlpatterns = [
    path('admin-login/' , views.adminLogin, name = 'adminLogin'),
    path('logout/' , views.logout_user, name= 'logout'),
    # path('dash/' , views.dash , name='dash'),
    path('export/', views.export_data, name='export_data'),
    path('export1/', views.raw_export_data, name='raw_export_data'),
    path('import_page/', views.import_page, name='import_page'),
    path('import/', views.import_data, name='import_data'),
    path('register/' , views.register , name = 'register'),
    path('user/' , views.userManage , name = 'user'),
    path('attendence1/' , views.attendence1, name = 'attendence1'),
    path('outReg/' , views.outReg, name = 'outReg'),
    path('outlet/' , views.outlet, name = 'outlet'),
    path('updateOutlet/<int:id>/' , views.updateOutlet, name = 'updateOutlet'),
    path('raw/' ,views.raw , name= 'raw'),
    path('check-out/' , views.checkout, name = 'check-out'),
    path('city/' , city , name = 'city'),
    path('add_city/' , add_city , name = 'add_city'),
   
]
