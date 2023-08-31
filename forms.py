from django import forms
from .models import UserLogin,AttendanceModel,CheckoutModel ,OutletModel , SupFormModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        
    