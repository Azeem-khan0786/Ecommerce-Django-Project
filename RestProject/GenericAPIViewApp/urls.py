
from GenericAPIViewApp import views 
from django.urls import path
urlpatterns = [
    path('generic_api_view/',views.ProductGenericAPIView.as_view(),name='generic_api_view'),
    path('generic_api_view/<int:pk>',views.ProductGenericAPIView.as_view(),name='generic_api_view'),

    path('generic_mixins/<int:pk>',views.CreateReadUpdateMixins.as_view(),name='generic_mixins'),
    path('generic_mixins/',views.CreateReadUpdateMixins.as_view(),name='generic_mixins'),

]