from django.contrib import admin
from .models import AttendanceModel , UserLogin , CheckoutModel , OutletModel ,SupFormModel
# Register your models here.
admin.site.register(AttendanceModel)
admin.site.register(UserLogin)
admin.site.register(CheckoutModel)
admin.site.register(OutletModel)
admin.site.register(SupFormModel)