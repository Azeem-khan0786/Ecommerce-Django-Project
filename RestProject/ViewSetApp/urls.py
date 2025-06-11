from django.contrib import admin
from django.urls import path,include
from ViewSetApp import views
from ViewSetApp.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product-viewset', ProductViewSet,basename='product')
router.register(r'product-modelviewset', ItemModelViewSet , basename='model_product'),
router.register(r'order-modelviewset', OrderModelViewSet , basename='model_order'),


urlpatterns = [
    path('', include(router.urls)),

]