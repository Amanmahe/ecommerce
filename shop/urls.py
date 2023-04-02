from django.urls import path
from . import views
urlpatterns = [
   path('', views.index, name="shophome"),
   path('about/', views.about, name="AboutUs"),
   path('contact/', views.contact, name="ContactUs"),
   path('tracker/', views.tracker, name="TrackingStatus"),
   path('search/', views.search, name="Search"),
   path('products/<int:myid>', views.productview, name="ProductView"),
   path('checkout/', views.checkout, name="CheckOut"),
   path('signup/',views.register,  name='reg'),
   path('check_user/',views.check_user,name='check_user'),
   path("user_login/",views.user_login, name="user_login"),
   path("cust_dashboard/",views.cust_dashboard, name="cust_dashboard"),
   path("seller_dashboard/",views.seller_dashboard, name="seller_dashboard"),
   ]
