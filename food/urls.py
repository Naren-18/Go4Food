from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('checkout',views.checkout,name='checkout'),
    path('coming_soon',views.coming_soon,name='coming_soon'),
    path('contact_us',views.contact_us,name='contact_us'),
    path('faq',views.faq,name='faq'),
    path('favorites',views.favorites,name='favorites'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('location',views.location,name='location'),
    path('login',views.login,name='login'),
    path('maintence',views.maintence,name='maintence'),
    path('map',views.map,name='map'),
    path('most_popular',views.most_popular,name='most_popular'),
    path('my_order',views.my_order,name='my_order'),
    path('not_found',views.not_found,name='not_found'),
    path('offers',views.offers,name='offers'),
    path('privacy',views.privacy,name='privacy'),
    path('profile',views.profile,name='profile'),
    path('restaurant',views.restaurant,name='restaurant'),
    path('search_restaurent',views.search_restaurent,name='search_restaurent'),
    path('signup',views.signup,name='signup'),
    path('status_canceled',views.status_canceled,name='status_canceled'),
    path('status_complete',views.status_complete,name='status_complete'),
    path('status_onprocess',views.status_onprocess,name='status_onprocess'),
    path('successful',views.successful,name='successful'),
    path('terms',views.terms,name='terms'),
    path('shipping_and_delivery',views.shipping_and_delivery,name='shipping_and_delivery'),

    path('cancelation_and_refund',views.cancelation_and_refund,name='cancelation_and_refund'),
    path('trending',views.trending,name='trending'),
    path('cod',views.cod,name='cod'),
    path('logout',views.logout,name='logout'),
    path('search_products',views.search_products,name='search_products'),
    
    
    # path('address_update',views.address_update,name='address_update'),
    path('profile_update',views.profile_update,name='profile_update'),
    
    path('verification',views.verification,name='verification'),
    
path('update_order',views.update_order,name='update_order'),
path('addcart',views.addcart,name='addcart'),
    path('removefromcart',views.removefromcart,name='removefromcart'),

      path('admin_users',views.admin_users,name='admin_users'),
    path('admin_orders',views.admin_orders,name='admin_orders'),
    path('admin_contact',views.admin_contact,name='admin_contact'),
    path('admin_restaurent',views.admin_restaurent,name='admin_restaurent'),
    path('admin_product',views.admin_product,name='admin_product'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    

    path('payment',views.payment,name='payment'),
    path('cartdetails',views.cartdetails,name='cartdetails'),
    path('payment_page/<int:data1>',views.payment_page,name="payment_page"),


    path('paymentsummary',views.paymentsummary,name="paymentsummary"),
    path('handlerequest/',views.handlerequest,name="handlerequest")
]