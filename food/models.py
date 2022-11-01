from email.policy import default
from django.db import models
from django.utils import timezone
import json

class Customers(models.Model):
    customer_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=20)
    number=models.CharField(max_length=12)
    password=models.CharField(max_length=30)
    address=models.TextField()
    area=models.CharField(max_length=30)
    No_of_orders=models.IntegerField(default=0)
    fav=models.CharField(max_length=500)
    cart=models.CharField(max_length=90)
    payment=models.CharField(default=False,max_length=30)

class Restaurent(models.Model):
    Restaurent_id = models.AutoField
    unique_restaurent_id=models.CharField(max_length=20,default="None")
    Restaurent_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    distance= models.IntegerField(default=10)
    Timing=models.CharField(max_length=20)
    image = models.ImageField(upload_to="food/static/img/restaurents", default="")
    type = models.CharField(max_length=20)
    def __str__(self):
        return self.Restaurent_name

class Product(models.Model):
    product_id = models.AutoField
    
    unique_product_id=models.CharField(max_length=20,default="None")
    product_name = models.CharField(max_length=50)
    
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    orginal_price=models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    available=models.IntegerField(default=1)
    pub_date = models.DateField()
    # image = models.ImageField(upload_to="food/static/img/products", default="")
    Restaurent_s=models.ForeignKey(
        Restaurent, on_delete=models.CASCADE,related_name='res')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")
    timestamp = models.DateTimeField(default=timezone.now)

    def str(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    razorpay_order_id=models.CharField(max_length=20)
    razorpay_payment_id=models.CharField(max_length=200)
    razorpay_signature=models.CharField(max_length=200)
    payment_status=models.CharField(max_length=200)
    items_json = models.JSONField(default=dict)
    userId_id = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    status=models.CharField(max_length=30,default="Ordered") 
 
    timestamp = models.DateTimeField(default=timezone.now)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=timezone.now)

    def str(self):
        return self.update_desc
