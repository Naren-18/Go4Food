

# import os;
# os.environ["OMP_NUM_THREADS"] = "1"

from ast import Num, Return
from ctypes import c_char

from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from functools import total_ordering
import numbers
from tabnanny import check
from urllib import response
from django.shortcuts import redirect, render 

from django.db import models
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.mail import send_mail

from django.db.models import F,Value,Count
from django.db.models.functions import Concat
from .models import Customers,Product,Restaurent,Orders,Contact
import pandas as pd
import json



@csrf_exempt
# Create your views here.
def home(request):
    products=Product.objects.all().values()
    restaurants_=Restaurent.objects.all().values()
    user={}
    context={
        'products':products,'user':user,'restaurant':restaurants_
    }
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        
    return render(request,'home.html',context)

def checkout(request):
    products_=Product.objects.all().values()
    user={}
    cart={}
    queryset={}
    if request.session.test_cookie_worked():
        records=pd.DataFrame(list(Customers.objects.filter(customer_id=request.COOKIES['customer_id'] ).values()))  
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        user['area']=records['area'][0]
        data=records.to_dict('dict')
        if records['address'].empty:
            pass
        else:
            
            user['address']=data['address'][0]
        # print()
        if records['cart'].empty:
            pass
        # else:
        #     cart_details=Customers.objects.filter(number=request.COOKIES['number']).values('cart')   
        #     lis=cart_details[0]['cart'].split(",")[:-1]
        #     queryset = pd.DataFrame(list(Restaurent.objects.select_related('res').filter(res__id__in=lis).values('res__id','res__product_name','res__price','Restaurent_name')))
        #     queryset['quantity']=queryset.apply(lambda row:lis.count(str(row['res__id'])),axis=1)
        #     print(queryset)
            # queryset=queryset.to_json(orient="records") 
            # x=list(data['cart'][0].split(","))
            # dict1=''.join(x)
            # all_freq={}
            # for i in dict1:
            #     if i in all_freq:
            #         all_freq[i] += 1
            #     else:
            #         all_freq[i] = 1
            # #print(all_freq)
            # for i in all_freq:
            #     #print(i)
            #     records=pd.DataFrame(list(Product.objects.filter(id=int(i)).values()))  
            #     data=records.to_dict('dict')
            #     product_name=data['product_name'][0]
            #     price=data['price'][0]
            #     image=data['image'][0]
            #     restaurant_id=data['Restaurent_s_id'][0]
            #     restaurents=pd.DataFrame(list(Restaurent.objects.filter(id=restaurant_id).values()))  
            #     data2=restaurents.to_dict('dict')
            #     restaurant_name=data2['Restaurent_name'][0]

            #     temp_lis=[image,product_name,price,all_freq[i],restaurant_name]
            #     cart[i]=temp_lis
            print("AAAAAA",queryset)
    return render(request,'checkout.html',{'products':products_,'user':user,'cart':queryset})
def coming_soon(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'coming-soon.html',{'products':products_,'user':user})
@csrf_exempt
def contact_us(request):
    products_=Product.objects.all().values()
    user={}
    msg=''
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        user['email']=request.COOKIES['email']
        if request.method == 'POST':
            Name=request.POST.get('name')
            Number=request.POST.get('number')
            Email=request.POST.get('email')
            Desc=request.POST.get('desc')
            contact=Contact()
            contact.name=Name
            contact.email=Email
            contact.desc=Desc
            contact.phone=Number
            contact.save()
            msg='Your Issue has been notified'
    return render(request,'contact-us.html',{'products':products_,'user':user,'msg':msg})
def faq(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user={
            'name':request.COOKIES['name'],
            'number':request.COOKIES['number'],
            'customer_id':request.COOKIES['customer_id']
    
        }
        
    return redirect('home')
def favorites(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'favorites.html',{'products':products_,'user':user})
@csrf_exempt
def forgot_password(request):
    products_=Product.objects.all().values()
    user={}
    msg=""
    if request.method == 'POST':
        Email=request.POST.get('email')
        records=pd.DataFrame(list(Customers.objects.filter(email=Email ).values()))
        if records.empty:
            msg="Account Does not Exists with This Email"
        else:
            data=records.to_dict('dict')
            name=data['name'][0]
            password=data['password'][0]
            subject = 'Your Password for Go4Food'
            message = f'Hi {name} Your Password is {password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[ Email]
            send_mail( subject, message, email_from, recipient_list )
            msg="Your Password has been sent to your email "


    return render(request,'forgot_password.html',{'products':products_,'user':user,'msg':msg})
def location(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'location.html',{'products':products_,'user':user})

@csrf_exempt
def login(request):
    products=Product.objects.all().values()
    restaurants_=Restaurent.objects.all().values()
    user={}
    context={
        
    }
    if request.session.test_cookie_worked():
        return redirect('home')
    if request.method == 'POST':
        Number=request.POST.get('number')
        Password=request.POST.get('password')
        # #print(Number,Password)
        if Number=='123456789' and Password=="Bhanu@123" :
            #print(Number,"fdfd")
            request.session.set_test_cookie()
            response=render(request,'admin_users.html')
            return response
        records=pd.DataFrame(list(Customers.objects.filter(number=Number,password=Password).values()))  
        if(records.empty):
            context={'msg':"*Inavlid Credentails*"}
            return render(request,'login.html',{'context':context})
        else:
            data=records.to_dict('dict')
            request.session.set_test_cookie()
            user={
                'name':data['name'][0],
                'customer_id':data['customer_id'][0],

            }
            products_=Product.objects.all().values()
            context={
                "products":products_
            }
            response=redirect('home')
            response.set_cookie("customer_id",data['customer_id'][0])
            response.set_cookie("number",data['number'][0])
            response.set_cookie("email",data['email'][0])
            response.set_cookie("address",data['address'][0])
            
            response.set_cookie("name",data['name'][0])
            return response
    return render(request,'login.html')
def logout(request):
    user={}
    if request.session.test_cookie_worked():
        
        request.session.delete_test_cookie()
        
        
        return redirect('home')
    else:
        return redirect('home')
def maintence(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'maintence.html',{'products':products_,'user':user})
def map(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'map.html',{'products':products_,'user':user})
def most_popular(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'most_popular.html',{'products':products_,'user':user})
def my_order(request):
    user={}
    #print(orders)
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        products_=Product.objects.all().values()
        # orders=Orders.objects.filter(userId_id=request.COOKIES['customer_id'],).values()
        orders1=Orders.objects.filter(userId_id=request.COOKIES['customer_id'],payment_status=1).values()
        orders2=Orders.objects.filter(userId_id=request.COOKIES['customer_id'],payment_status='cod').values()
        orders=orders1 | orders2
        return render(request,'my_order.html',{'products':products_,'user':user,'orders':orders})
    else:
        return redirect('login')
def not_found(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'not-found.html',{'products':products_,'user':user})
def offers(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'offers.html',{'products':products_,'user':user})
def privacy(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'privacy.html',{'products':products_,'user':user})

def shipping_and_delivery(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'shipping_and_delivery.html',{'products':products_,'user':user})

def terms(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'terms.html',{'products':products_,'user':user})
def cancelation_and_refund(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'cancelation_and_refund.html',{'products':products_,'user':user})

def profile(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        records=pd.DataFrame(list(Customers.objects.filter(customer_id  =request.COOKIES['customer_id']).values()))  
        data=records.to_dict('dict')
        user['name']=data['name'][0]
        user['email']=data['email'][0]
        user['customer_id']=data['customer_id'][0]
        user['number']=data['number'][0]
        user['address']=data['address'][0]
        user['No_of_orders']=data['No_of_orders'][0]
    return render(request,'profile.html',{'products':products_,'user':user})


def restaurant(request):
    products_=Product.objects.all().values()
    user={}
    res_id = request.GET.get('data')
    res_products=Product.objects.filter(Restaurent_s_id=res_id).values()
    restuarant_details=Restaurent.objects.filter(id=res_id).values()
    #print(res_products)
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'restaurant.html',{'products':res_products,'user':user,'restaurentdetails':restuarant_details})

@csrf_exempt
def search_restaurent(request):
    restaurants_=Restaurent.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'search.html',{'user':user,'restaurant':restaurants_})

@csrf_exempt
def search_products(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'search.html',{'user':user,'products':products_})

@csrf_exempt
def signup(request):
    user={}
    if request.method == 'POST':
        msg=''
        Name=request.POST.get('name')
        Number=request.POST.get('number')
        Password=request.POST.get('password')
        Email=request.POST.get('email')
        Address=request.POST.get('address')
        Area=request.POST.get('Area')
        if request.POST.get('name')=='' or request.POST.get('password')=='' or request.POST.get('address')=='' :
            msg="Fill all the details to Register"
        elif request.POST.get('terms')==None or request.POST.get('privacy')==None:
            msg="Accept Terms and our privacy policy"
            
        else:
            if len(Number)==10:
                records=pd.DataFrame(list(Customers.objects.filter(number=Number).values()))  
                if(records.empty):
                    
                    records2=pd.DataFrame(list(Customers.objects.filter(email=Email).values()))  
                    if(records2.empty):
                        user=Customers()
                        user.name=Name
                        user.password=Password
                        user.number=Number
                        user.email=Email
                        user.address=Address
                        user.area=Area
                        user.save()
                        subject = 'Greetings from GO4FOOD'
                        message = f'Hi {Name}, Thankyou for choosing our service We will be waiting for your orders'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list =[ Email]
                        send_mail( subject, message, email_from, recipient_list )
                        msg='Registration Succesful'
                        return render(request,'login.html',{'msg':msg})
                    else:
                        msg="Email already exists"
                else:
                    msg="Phone number already exists "
            else:
                msg="Invalid Phone Number"
        return render(request,'signup.html',{'msg':msg})
    return render(request,'signup.html')
def status_canceled(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        
    return render(request,'status_canceled.html',{'products':products_,'user':user})
def status_complete(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        
    return render(request,'status_complete.html',{'products':products_,'user':user})
def status_onprocess(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'status_onprocess.html',{'products':products_,'user':user})

@csrf_exempt    
def successful(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'successful.html',{'products':products_,'user':user})
def trending(request):
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    return render(request,'trending.html',{'products':products_,'user':user})
def verification(request):
    
    products_=Product.objects.all().values()
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
         
    return render(request,'verification.html',{'products':products_,'user':user})





@csrf_exempt
def profile_update(request):
    Name=request.POST.get('name')
    
    Address=request.POST.get('address')
    
    Area=request.POST.get('area')
    print("AAAAAA",Area)
    user=Customers.objects.get(customer_id=request.COOKIES['customer_id'])
    user.name=Name
    user.address=Address
    user.area=Area
    user.save()
    return redirect('profile')

# ajax request functions
 

@csrf_exempt 
def addcart(request):
    if request.session.test_cookie_worked():
        
        id=request.POST.get('id')
        Customers.objects.filter(number=request.COOKIES['number']).update(cart=Concat(F('cart'),Value(id),Value(',')))
        cart_details=Customers.objects.filter(number=request.COOKIES['number']).values('cart')   
        lis=cart_details[0]['cart'].split(",")[:-1]
        queryset = pd.DataFrame(list(Restaurent.objects.select_related('res').filter(res__id__in=lis).values('res__id','res__product_name','res__price','Restaurent_name')))
        queryset['quantity']=queryset.apply(lambda row:lis.count(str(row['res__id'])),axis=1)
        queryset=queryset.to_json(orient="records")
        
        #print(queryset)
        return JsonResponse({'cartitems':json.loads(queryset)})   
    else:
        return redirect('login')
@csrf_exempt 
def removefromcart(request):
    
    id=request.POST.get('id')
    cart_details=Customers.objects.filter(number=request.COOKIES['number']).values('cart') 
    lis=cart_details[0]['cart'].split(",")
    lis.remove(str(id))
    Customers.objects.filter(number=request.COOKIES['number']).update(cart=','.join(lis))
    cart_details=Customers.objects.filter(number=request.COOKIES['number']).values('cart')   
    lis=cart_details[0]['cart'].split(",")[:-1]
    queryset = pd.DataFrame(list(Restaurent.objects.select_related('res').filter(res__id__in=lis).values('res__id','res__product_name','res__price','Restaurent_name')))
    queryset['quantity']=queryset.apply(lambda row:lis.count(str(row['res__id'])),axis=1)
    queryset=queryset.to_json(orient="records")
    
    #print(queryset)
    return JsonResponse({'cartitems':json.loads(queryset)}) 

def admin_users(request):
    
    if request.session.test_cookie_worked():
        total_orders=Orders.objects.count()
        present_orders1=Orders.objects.filter(status ="Ordered").count()
        present_orders2=Orders.objects.filter(status ="Order Conformed").count()
        present_orders3=Orders.objects.filter(status ="Enroute").count()

        res=Customers.objects.count()
        context={
            'customers':res,
            'total_orders':total_orders,
            'present_orders':present_orders1+present_orders2+present_orders3
        }
        return render(request,'admin_users.html',{'context':context})
    else:
        redirect('login')

def admin_orders(request):

    if request.session.test_cookie_worked():
        orders_1=Orders.objects.filter(payment_status=1).values()
        orders_2=Orders.objects.filter(payment_status='cod').values()
        orders_=orders_1 | orders_2 
        orders=pd.DataFrame(list(Orders.objects.filter(payment_status='1').values()))
        data=orders.to_dict('dict')
        #print(orders_)
        return render(request,'admin_orders.html',{'orders':orders_})
    else:
        redirect('login')

def admin_contact(request):
    
    if request.session.test_cookie_worked():
        return render(request,'admin_contact.html')
    else:
        redirect('login')

def admin_restaurent(request):
    
    if request.session.test_cookie_worked():
        restaurant=Restaurent.objects.all().values()
        #print(restaurant)
        return render(request,'admin_restaurent.html',{'restaurant':restaurant})
    else:
        redirect('login')
    
def admin_product(request):
    
    if request.session.test_cookie_worked():
        products=Product.objects.all().values()

        return render(request,'admin_product.html',{'products':products})
    else:
        redirect('login')

def admin_logout(request):
    request.session.delete_test_cookie()
    return redirect('home')
@csrf_exempt
def update_order(request):
    status=request.POST.get('status')
    order_id=request.POST.get('order_id')
    Orders.objects.filter(order_id=order_id).update(status=status)
    return redirect('admin_orders')
import razorpay
razorpay_client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

from django.contrib.sites.shortcuts import get_current_site
@csrf_exempt    
def payment(request):
    user={}
    final_dict={}
    total_price=0
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
        user['email']=request.COOKIES['email']
        products=json.loads(request.POST.get('products')) 
        total_price=request.POST.get('total')
        products_=pd.DataFrame(list(Product.objects.all().values()))
        final_dict={}  #{'product_id':[times,name,price,restaurent_id]}
        c=0
        
        data=products_.to_dict('dict')
        tem_str=""
        for i in products:
            lis=[]
            ass=pd.DataFrame(list(Product.objects.filter(id=i).values()))
            temp=ass.to_dict('dict')
            # #print(temp)

            if int(i)==temp['id'][0]: 
                item_price=int(products[i])*int(temp['price'][0])
                # total_price=total_price+item_price
                restaurents=pd.DataFrame(list(Restaurent.objects.filter(id=temp['Restaurent_s_id'][0]).values()))
                restaurant_data=restaurents.to_dict('dict')
                restaurant_name=restaurant_data['Restaurent_name'][0]
                restaurant_address=restaurant_data['address'][0]
                
                lis=[products[i],temp['product_name'][0],temp['price'][0],temp['Restaurent_s_id'][0],item_price,restaurant_name,restaurant_address]
                final_dict[i]=lis
        orders=Orders()
        orders.items_json=final_dict
        orders.userId_id=request.COOKIES['customer_id']
        orders.amount=total_price
        orders.email=request.COOKIES['email']
        orders.address=request.COOKIES['address']
        orders.phone=request.COOKIES['number']
        orders.zip_code="NULL"
        orders.save()
        
        order_currency = 'INR'

        callback_url = 'https://go4food.online/handlerequest/'
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=int(total_price)*100, currency=order_currency, notes = notes, receipt=str(orders.order_id), payment_capture=1))
        orders.razorpay_order_id = razorpay_order['id']
        orders.save()
        
        return render(request,'payment/paymentsummary.html',{'order':orders,'final_dict':final_dict, 'order_id': razorpay_order['id'], 'orderId':orders.order_id, 'final_price':total_price, 'razorpay_merchant_id':settings.KEY_ID, 'callback_url':callback_url,'user':user})     
    else:
        return redirect('login')
@csrf_exempt
def cod(request,):
    user={}
    if request.session.test_cookie_worked():
        user['name']=request.COOKIES['name']
        user['customer_id']=request.COOKIES['customer_id']
        user['number']=request.COOKIES['number']
    orderid=request.POST.get('orderid')
    Orders.objects.filter(order_id=orderid).update(payment_status='cod')
    print("AAA",orderid)
    Customers.objects.filter(number=request.COOKIES['number']).update(cart='')
    # order.payment_status="COD"
    return render(request, 'successful.html',{'id':orderid,'user':user})
def payment_page(request,data):
    #print(data)
    return render(request,'payment.html')
@csrf_exempt
def cartdetails(request):
    cart_details=Customers.objects.filter(number=request.COOKIES['number']).values('cart')   
    lis=cart_details[0]['cart'].split(",")[:-1]
    queryset = pd.DataFrame(list(Restaurent.objects.select_related('res').filter(res__id__in=lis).values('res__id','res__product_name','res__price','Restaurent_name')))
    queryset['quantity']=queryset.apply(lambda row:lis.count(str(row['res__id'])),axis=1)
    queryset=queryset.to_json(orient="records") 
    return JsonResponse({'cartitems':json.loads(queryset)})


def paymentsummary(request):
    pass

from django.core.mail import EmailMultiAlternatives
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id','')
        signature = request.POST.get('razorpay_signature','')
        params_dict = { 
        'razorpay_order_id': order_id, 
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
        }
        # print(params_dict)
        try:
            order_db = Orders.objects.get(razorpay_order_id=order_id)
        except:
            return HttpResponse("505 Not Found")
        order_db.razorpay_payment_id = payment_id
        order_db.razorpay_signature = signature
        order_db.save()
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result==True:
            amount = order_db.amount * 100   #we have to pass in paisa
            # try:
            order_db.payment_status = 1
            order_db.save()
            
            Customers.objects.filter(number=request.COOKIES['number']).update(cart='')
            ## For generating Invoice PDF
            # template = get_template('payment/invoice.html')
            # data = {
            #     'order_id': order_db.order_id,
            #     'transaction_id': order_db.razorpay_payment_id,
            #     'user_email': order_db.email,
            #     # 'date': str(order_db.datetime_of_payment),
            #     'name': order_db.name,
            #     'order': order_db,
            #     'amount': order_db.amount,
            # }
            # html  = template.render(data)
            # result = BytesIO()
            # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)#, link_callback=fetch_resources)
            # pdf = result.getvalue()
            # filename = 'Invoice_' + data['order_id'] + '.pdf'
            # mail_subject = 'Recent Order Details'
            # message = render_to_string('firstapp/payment/emailinvoic.html', {
            #     'user': order_db.user,
            #     'order': order_db
            # })
            context_dict = {
                'user': order_db.name,
                'order': order_db
            }
            # template = get_template('payment/emailinvoice.html')
            # message  = template.render(context_dict)
            # to_email = order_db.user.email
            # email = EmailMessage(
            #     mail_subject,
            #     message, 
            #     settings.EMAIL_HOST_USER,
            #     [to_email]
            # )
            # for including css(only inline css works) in mail and removeautoescape off
            # email = EmailMultiAlternatives(
            #     mail_subject,
            #     "hello",       # necessary to pass some message here
            #     settings.EMAIL_HOST_USER,
            #     [to_email]
            # )
            # email.attach_alternative(message, "text/html")
            # email.attach(filename, pdf, 'application/pdf')
            # email.send(fail_silently=False)
            return render(request, 'successful.html',{'id':order_db.order_id})
            # except Exception:
            #     order_db.payment_status = 2
            #     order_db.save()
            #     print(Exception)
            #     return render(request, 'payment/paymentfailed.html')
        else:
            order_db.payment_status = 2
            order_db.save()
            return render(request, 'payment/paymentfailed.html')
        # except:
        #     return HttpResponse("505 not found")
