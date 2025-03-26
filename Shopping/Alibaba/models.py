from django.db import models
from django.contrib.auth.models import User

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
        return self.name + " " + self.location
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
    composition = models.TextField( blank=True,null=True)

    def __str__(self):
        return f"{self.title}"

    
   
    


# models for add cart 
class CartItemModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f'{self.quantity} * {self.product.title}'

class PaymentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BinaryField()

class OrderPlacedModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(CustomerModel,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_created=True)
    quantity=models.PositiveIntegerField(default=1)
    status=models.CharField(max_length=50,choices=STATE_CHOICES,default='Pending')
    payment=models.ForeignKey(PaymentModel,on_delete=models.CASCADE,default='')
    @property
    def total_cost(self):
        return self.quantity * self.product.discount