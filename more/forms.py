from django import forms
from .models import UserLogin,AttendanceModel,CheckoutModel ,OutletModel , SupFormModel, CityModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=10)
    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1' , 'password2')





class UserForm(forms.ModelForm):
    
    class Meta:
        model = UserLogin
        fields = '__all__'
        
class AttendanceForm(forms.ModelForm):
    
    class Meta:
        model = AttendanceModel
        fields = '__all__'
        
   
        
class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = CheckoutModel
        fields = '__all__'
        
        
class OutletForm(forms.ModelForm):
    class Meta:
        model = OutletModel
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        
        if OutletModel.objects.filter(code=code).exclude(id=self.instance.id).exists():
            self.add_error('code', "Code is already registered.")
            
class SupForm(forms.ModelForm):
    class Meta:
        model = SupFormModel
        fields = '__all__'
        
class CityForm(forms.ModelForm):
    

    class Meta:
        model = CityModel  
        fields = ['city']

    def clean_dob(self):
        city = self.cleaned_data.get('city')
        city1 = CityModel.objects.all()
        
        for i in city1:
            if i==city:
                raise ValidationError('City Already Registered')
        return city