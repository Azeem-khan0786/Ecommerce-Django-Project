from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
   list_display=('id','title',"selling_price","discount","catagory","product_image")


admin.site.register(ProductModel, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
   list_display=('user','name',
   'location',
    'city',
    'mobile',
    'zipcode',
    'state' )
   
admin.site.register(CustomerModel,CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
   list_display=['product','quantity']
admin.site.register(CartItemModel,CartAdmin)   

class PaymentAdmin(admin.ModelAdmin):
   list_display=['user','amount',"razorpay_order_id",'razorpay_payment_status','paid']
admin.site.register(PaymentModel,PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
   list_display=['user','customer','product','ordered_date','quantity','status','payment']
admin.site.register(OrderPlacedModel,OrderAdmin)                   