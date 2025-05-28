from django.contrib import admin
from Alibaba.models import *

# admin email =azeemkhan@xyz.in with 1234 username =khan
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
   list_display=('id','category','title',"selling_price","discount","product_image")


admin.site.register(ProductModel, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
   list_display=('user','name',
   'location',
    'city',
    'mobile',
    'zipcode',
    'state' )
   
admin.site.register(CustomerModel,CustomerAdmin)
admin.site.register(Cart)
class CartAdmin(admin.ModelAdmin):
   list_display=['product','quantity','date_added']
admin.site.register(CartItem,CartAdmin)   

admin.site.register(Category)

admin.site.register(Payment)

# class OrderAdmin(admin.ModelAdmin):
#    list_display=['user','customer','product','ordered_date','quantity','status','payment']
# admin.site.register(OrderPlacedModel,OrderAdmin)       
# 
class OrderAdmin(admin.ModelAdmin):
   list_display=['id','user','status','get_count','get_all_order_items']
admin.site.register(Order,OrderAdmin) 

admin.site.register(OrderItem)          
admin.site.register(Address)  
  

