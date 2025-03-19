"""
URL configuration for Shopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Alibaba import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment_success',views.payment_success,name='payment_success'),
    path('payment_failed',views.payment_failed,name='payment_failed'),

    path('',views.home,name='home'),
    path('about',views.aboutUs,name='about'),
    path('contact',views.contactUs,name='contact'),
    path('catagory/<slug:val>',views.CatagoryView.as_view(),name='catagory'),
    path('productDetail/<int:pk>',views.ProductView.as_view(),name='productDetail'),
    path('registration/',views.RegistrationView.as_view(),name="registration"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout_request/',views.logout_request,name='logout'),
    path('address/',views.address,name='address'),
    path('updateProfile/<int:pk>',views.UpdateProfile.as_view(),name="updateProfile"),
    path('changepassword/',views.ChangePasswordView.as_view(),name='changepassword'),
    path('addcart/<int:product_id>',views.add_cart,name='addcart'),
    path('viewcart/',views.view_cart,name='viewcart'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('search/',views.product_search, name='product_search'),
    path('removecart/<int:item_id>',views.remove_from_cart,name='removecart'),
    path('paypal/', include("paypal.standard.ipn.urls")),  # ins=clude paypal view`s url`
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
