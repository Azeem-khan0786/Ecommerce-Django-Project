from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
# Create your models here.
Catagories_Choice=(('PNT','pents'),
                   ('ST','Shirts'),
                   ('SO','Shoes'),
                   
                   ('SA','Sarees'),
                   ('WA','Wallets'),
                     )
# field for CustomerModel 
STATE_CHOICES=(('AP' , 'Andhra Pradesh'),
('AR' , 'Arunachal Pradesh'),
('AS' , 'Assam'),
('BR' , 'Bihar'),
('CT' , 'Chhattisgarh'),
('GA' , 'Goa'),
('GJ' , 'Gujarat'),
('HR' , 'Haryana'),
('HP' , 'Himachal Pradesh'),
('JK' , 'Jammu and Kashmir'),
('JH' , 'Jharkhand'),
('KA' , 'Karnataka'),
('KL' , 'Kerala'),
('MP' , 'Madhya Pradesh'),
('MH' , 'Maharashtra'),
('MN' , 'Manipur'),
('ML' , 'Meghalaya'),
('MZ' , 'Mizoram'),
('NL' , 'Nagaland'),
('OR' , 'Odisha'),
('PB' , 'Punjab'),
('RJ' , 'Rajasthan'),
('SK' , 'Sikkim'),
('TN' , 'Tamil Nadu'),
('TG' , 'Telangana'),
('TR' , 'Tripura'),
('UT' , 'Uttarakhand'),
('UP' , 'Uttar Pradesh'),
('WB' , 'West Bengal'),
('AN' , 'Andaman and Nicobar Islands'),
('CH' , 'Chandigarh'),
('DN' , 'Dadra and Nagar Haveli'),
('DD' , 'Daman and Diu'),
('DL' , 'Delhi'),
('LD' , 'Lakshadweep'),
('PY' , 'Puducherry'),
)

class CustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES)

    def __str__(self): # Here
        return self.name + " " + self.locationOrderItem
    class Meta:
        unique_together=('user',)
# method for create category        
class Category(models.Model):
    name = models.CharField(max_length=20,default='1')

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    def __str__(self):
        return self.name        
        
class ProductModel(models.Model):
    title = models.CharField(max_length=70)
    selling_price = models.FloatField()
    discount = models.FloatField()
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)  # New ForeignKey
    product_image = models.ImageField(upload_to='proImage', blank=True, null=True)
    # product_image = models.URLField()  # Ensure it's a URLField, not ImageField!
    composition = models.TextField( blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
    # retrive all product 
    @staticmethod
    def get_products():
        return ProductModel.objects.all()
    
    # retrive all product based on category
    @staticmethod
    def get_products_by_category(category_id):
        return ProductModel.objects.filter(category_id=category_id)
    
# model Order 
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email= models.EmailField(max_length=30)
    shipping_adress = models.TextField(max_length=255)
    amount_paid= models.DecimalField(max_digits=5,decimal_places=2)
    shipping_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=datetime.now(), blank=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'ShippingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'ShippingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order place by {self.user}"
    
# model OrderItem for indivitual item
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)   
    price = models.DecimalField( max_digits=5, decimal_places=2)

    # def __str__(self):
    #     pass

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.address_line}, {self.city}'    

# models for add cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def get_total_price(self):
        return self.product.price * self.quantity

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# class OrderPlacedModel(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     customer=models.ForeignKey(CustomerModel,on_delete=models.CASCADE)
#     product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
#     ordered_date=models.DateTimeField(auto_created=True)
#     quantity=models.PositiveIntegerField(default=1)
#     status=models.CharField(max_length=50,choices=STATE_CHOICES,default='Pending')
#     payment=models.ForeignKey(PaymentModel,on_delete=models.CASCADE,default='')
#     @property
#     def total_cost(self):
#         return self.quantity * self.product.discount