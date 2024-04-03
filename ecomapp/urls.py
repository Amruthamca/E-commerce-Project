from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login1',views.login1,name='login1'),
    path('signup',views.signup,name='signup'),
    path('add_details',views.add_details,name='add_details'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('add_cate',views.add_cate,name='add_cate'),
    path('add_cate_details',views.add_cate_details,name='add_cate_details'),
    path('add_pro',views.add_pro,name='add_pro'),
    path('add_pro_details',views.add_pro_details,name='add_pro_details'),
    path('view_product',views.view_product,name='view_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('view_user_details/', views.view_user_details, name='view_user_details'),
    path('delete_user/<int:pk>',views.delete_user,name="delete_user"),
    path('logout1',views.logout1,name='logout1'),
    path('user_home',views.user_home,name='user_home'),
    path('productlist/<int:pk>',views.productlist,name="productlist"),
    path('view_productlist/<int:pk>/', views.view_productlist, name='view_productlist'),
    #path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    #path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
   
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'), 
    path('cart/', views.cart, name='cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_item/', views.remove_item, name='remove_item'),  
    path('place_order',views.place_order,name="place_order"),
    path('confirm_message',views.confirm_message,name="confirm_message")
]