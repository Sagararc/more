from django.db import models


class UserLogin(models.Model):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class AttendanceModel(models.Model):
  
    user = models.CharField(max_length=100,blank=True , null=True)
    username = models.CharField(max_length=100,blank=True , null=True)
    checkin = models.CharField(max_length=100,blank=True , null=True)
    checkin_image = models.ImageField(upload_to='checkin/',null=True, default="",blank=True)
    lat = models.CharField(max_length=100 , blank=True , null=True,default=0.0)
    long = models.CharField(max_length=100 , blank=True , null=True ,default=0.0)
    flag = models.CharField(max_length=100 , blank=True , null=True ,default= 0)
   
    
    
    def __str__(self):
        return f"{self.user} - {self.checkin}"
    

class CheckoutModel(models.Model):
  
    user = models.CharField(max_length=100,blank=True , null=True)
    username = models.CharField(max_length=100,blank=True , null=True)
    checkout = models.CharField(max_length=100,blank=True , null=True)
    checkout_image = models.ImageField(upload_to='checkin/',null=True, default="",blank=True)
    lat = models.CharField(max_length=100 , blank=True , null=True,default=0.0)
    long = models.CharField(max_length=100 , blank=True , null=True ,default=0.0)
   

    def __str__(self):
        return f"{self.user} - {self.checkout}"
    


class OutletModel(models.Model):
    
    
    name = models.CharField(max_length=100 , blank=True , null=True )
    code = models.CharField(max_length=100 , blank=True , null=True ,unique=True)
    address = models.CharField(max_length=100 , blank=True , null=True )
    lat = models.CharField(max_length=100 , blank=True , null=True  )
    long = models.CharField(max_length=100 , blank=True , null=True  )
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    
    
    def __str__(self):
        return self.name
    
class SupFormModel(models.Model):
    

    
    confi_choice = [
        ('1' , '1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    ]
    
    user = models.CharField(max_length=100,blank=True , null=True)
    username = models.CharField(max_length=100,blank=True , null=True)
    outlet = models.ForeignKey(OutletModel , on_delete=models.CASCADE)
    moname = models.CharField(max_length=100,blank=True , null=True)
    uniform = models.CharField(max_length=100 , blank=True , null=True)
    grooming = models.CharField(max_length=100 , blank=True , null=True)
    ol = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    po = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    sfm = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    sapp = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    leaf = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    dapp = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    script = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    confi = models.CharField(max_length=10, choices=confi_choice)
    calls = models.CharField(max_length=400 , blank=True , null=True)
    ps =  models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    lat = models.CharField(max_length=100 ,blank=True , null=True)
    long = models.CharField(max_length=100 ,blank=True , null=True)
    ts = models.CharField(max_length=100 ,blank=True , null=True)
    remark = models.CharField(max_length=100 ,blank=True , null=True)

    def __str__(self):
        return self.username