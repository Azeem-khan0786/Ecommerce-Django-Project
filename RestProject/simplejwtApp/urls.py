
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from simplejwtApp import views

urlpatterns = [
    # Your URLs...
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', views.HomeView.as_view(), name='home'),

]