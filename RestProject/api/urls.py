from django.contrib import admin
from django.urls import path
from api import views
app_name = 'api'
urlpatterns = [
    
    path('products',views.products,name='products'), 
    path('single_product/<int:pk>/',views.single_product,name='single_product'),
    path('order_view',views.OrderView.as_view(),name= 'order_view'),
    path('createproduct_view',views.CreateProduct.as_view(),name= 'createproduct_view'),
    path('order_status_view/<str:order_status>/',views.OrderViaStatus.as_view(),name= 'order_view')

]