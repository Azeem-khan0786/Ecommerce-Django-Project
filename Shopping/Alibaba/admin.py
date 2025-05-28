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
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display=['id','user','status','payment_option', 'ordered_date','get_count','get_all_order_items']
   list_filter=['status','payment_option']
   actions = ['mark_as_shipped', 'mark_as_delivered']
    
   def mark_as_shipped(self, request, queryset):
      for order in queryset:
            if order.payment_option == 'COD':
               order.update_status('shipped')
            elif order.payment_option == 'P':
               order.update_status('processing')
   mark_as_shipped.short_description = "Mark selected orders as shipped"
   
   def mark_as_delivered(self, request, queryset):
      for order in queryset:
            order.update_status('delivered')
            if order.payment_option == 'COD':
               order.create_payment_record()
   mark_as_delivered.short_description = "Mark selected orders as delivered"
 

admin.site.register(OrderItem)          
admin.site.register(Address)  
  

