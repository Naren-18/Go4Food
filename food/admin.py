from django.contrib import admin

# Register your models here.
from .models import Restaurent,Product,Customers
admin.site.register(Restaurent)
admin.site.register(Product)
admin.site.register(Customers)