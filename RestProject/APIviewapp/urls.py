from django.contrib import admin
from django.urls import path
from APIviewapp import views
from APIviewapp.views import *
urlpatterns = [
    
    path('products_api/',ProductClassBasedView.as_view(),name='products-api'), 
    path('products_details/<int:pk>',ProductClassBasedViewDetails.as_view(),name='products-details'), 

    # path('single_product/<int:pk>/',views.single_product,name='single_product'),
    # path('order_view',views.OrderView.as_view(),name= 'order_view'),
    # path('order_status_view/<str:order_status>/',views.OrderViaStatus.as_view(),name= 'order_view')

]