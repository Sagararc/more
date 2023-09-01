from django.urls import path 
from django.contrib.auth.views import LoginView
from .views import login_view,dash,attendance,supForm,checkout,logout_user,success
urlpatterns = [
    path('' , login_view , name='login'),
    path('logout/' , logout_user, name= 'logout'),
    path('dash/' , dash , name='dash'),
    path('attendance/' , attendance , name='attendance'),
    path('checkout/' , checkout , name='checkout'),
    path('form/' , supForm , name='supForm'),
    path('success/' , success , name='success'),
   
   
]
