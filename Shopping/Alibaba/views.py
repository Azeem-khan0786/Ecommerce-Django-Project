from django.shortcuts import render,redirect ,get_object_or_404
from .models import ProductModel,Category,CustomerModel,OrderItem,Order ,ShippingAddress,CartItem
from django.views import View
from .forms import RegistrationForm,LoginForm,CustomerProfileForm,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy , reverse 
from django.http import JsonResponse
from .forms import CheckoutForm ,ShippingAddressForm
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user_id for duplicate user
from django.core.exceptions import ObjectDoesNotExist
from Alibaba.serializers import ProductSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

def home(request):
    products =ProductModel.get_products()
    
    categories = Category.objects.all()
    Category_id=request.GET.get('category')
    print(Category_id)
    if Category_id:
        products = ProductModel.get_products_by_category(Category_id)     

    else:
        products = ProductModel.get_products()     
    # filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if max_price and min_price:
       products = products.filter(selling_price__gte=min_price,selling_price__lte=max_price)

    # Filter by availability (example)
    available = request.GET.get('available')
    if available == 'true':
        products = products.filter(stock_quantity__gt=0)
    elif available == 'false':
            products = products.filter(stock_quantity=0)

    data={
        'products': products,
        'categories': categories
    }

    return render(request,'Alibaba/home.html', data )


# ChangePasswordForm
def displayPost(request):
    item=ProductModel.objects.all()
    return render(request,'Alibaba/displayPost.html',{'item':item})

class CategoryView(View):
    def get(self,request,val):
        productlist=ProductModel.objects.filter(category=val)
        print(productlist)
        # title=ProductModel.objects.filter(category=val).values("title")
        data=ProductModel.objects.filter(category=val).values('title')
        # print(data.title)
        return render(request,"Alibaba/category.html",locals())
    # create post 
    def post(self,request):
        pass
class ProductDetail(View):
    def get(self,request,pk):
        data = get_object_or_404(ProductModel,pk=pk)
        return render(request,'Alibaba/productDetail.html',{'data':data})

# for json Data     
# class ProductView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def get(self,request):
#         product_details = ProductModel.objects.all()
#         serializer = ProductSerializer(product_details,many = True)
#         return Response(serializer.data)  
#     def post(self,request):
#         serializer = ProductSerializer(data = request.data,many = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

class CategoryView(APIView):
    def get(self,request):
        category_details = Category.objects.all()
        serializer = CategorySerializer(category_details,many = True)
        return Response(serializer.data)    
    def post(self,request):
        serializer = CategorySerializer(data = request.data,many =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class RegistrationView(View):
    def get(self,request):
        form=RegistrationForm()
        return render(request,"Alibaba/registration.html",context={"register_form":form})
    def post(self,request):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration has been completed!!!!!!!!!!')
        else:
            messages.warning(request, "Data was not inserted")
        return render(request,"Alibaba/registration.html",context={"register_form":form})
        
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        messages = ''  # Initialize messages (if needed)
        return render(request, 'Alibaba/login.html', context={'login_form': form, 'messages': messages})

    def post(self, request):
        form = LoginForm(request.POST)
         # Initialize messages (if needed)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request,f'Hello {user.username}! You have been logged in')
                return redirect('home')  # Redirect to home page upon successful login
            else:
                messages.warning(request,'Login Failed!')
            
        else:
            # Form is invalid, re-render the login page with form and error messages
            return render(request, 'Alibaba/login.html', context={"login_form": form, 'messages': messages})

        # Ensure a response is returned in all scenarios
        return render(request, 'Alibaba/login.html', context={"login_form": form, 'messages': messages})          
class ProfileView(View):
    def get(self,request):
        messages=''
        form=CustomerProfileForm()
        return render(request,'Alibaba/profile.html',context={"profile_form":form,"message":messages})
    def post(self,request):
        if request.method=='POST':
            form=CustomerProfileForm(request.POST)
            if form.is_valid():
                user=request.user
                name=form.cleaned_data['name']
                location=form.cleaned_data['location']
                city=form.cleaned_data['city']
                mobile=form.cleaned_data['mobile']
                state=form.cleaned_data['state']
                zipcode=form.cleaned_data['zipcode']
                data=CustomerModel(user=user,name=name,location=location,city=city,mobile=mobile,state=state,zipcode=zipcode)

                data.save()
                print(data)
                messages.success(request,'Profile created sucessfully!!')
            else:
                messages.warning(request,'Profile cannot create ')
            return render(request,'Alibaba/profile.html',context={"profile_form":form,"message":messages})

class makeOrder(View):
    def get(self,request):
        orders = Order.objects.filter(user=request.user)
        return render(request,'Alibaba/orderPage.html',context={'orders':orders})

def logout_request(request):
    logout(request)
    messages.info(request,'You have been logged Out!!!')
    return redirect('home')    
class UpdateProfile(View):
    def get(self,request,pk):
        add=CustomerModel.objects.get(user=pk)
        form=CustomerProfileForm(instance=add)
        print(form)
        return render(request,'Alibaba/updateprofile.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        print('get Form Herer',form)
        if form.is_valid():
            add=CustomerModel.objects.get(user_id=pk)
            add.name=form.cleaned_data['name']
            add.location=form.cleaned_data['location']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.zipcode=form.cleaned_data['zipcode']
            add.state=form.cleaned_data['state']
            add.save()
            print(add)
            messages.success(request,'Profile updated successfully!')
            return redirect('address')
        else:
            messages.warning('Enter data is not valid')    
        return render(request,'Alibaba/updateprofile.html',locals())    

        # print(add)

# Password change View
class ChangePasswordView(View):
    def get(self,request):
        form=ChangePasswordForm(request.user)
        return render(request,'Alibaba/changePassword.html',context={'form':form})    
    def post(self,request):
        form=ChangePasswordForm(request.user,request.POST)
        print(form)
        if form.is_valid():
            new_password1=form.cleaned_data['new_password1']
            form.save()
            messages.success(request,'Password Change Successfully')
            redirect ('home')
        else:
            messages.warning(request,'Password  incorrect!')
        return render(request,'Alibaba/changePassword.html',locals())

@login_required(login_url=reverse_lazy('login'))
def add_cart(request, product_id):
    product = ProductModel.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    # print(cart_item.quantity)
    cart_item.save()
    return redirect('viewcart')

def view_cart(request):
    cart_item = CartItem.objects.filter(user=request.user)
    amount = 0
    
    for item in cart_item:
        value = item.product.selling_price * item.quantity
        amount += value
    count=len(cart_item)
    total_amount = amount + 40
    
    return render(request, 'Alibaba/cart.html',locals())
    
class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            address_id =self.request.session.get('seleceted_id')
            if address_id:
                shipping_adress = ShippingAddress.objects.get(id=address_id,user=self.request.user)

            else:
                shipping_adress = ShippingAddress.objects.filter(user=self.request.user).first()
            form = CheckoutForm()
            context = {
                'form': form,
                # 'couponform': CouponForm(),
                'order': order,
                'shipping_adress':shipping_adress,
                # 'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "Alibaba/checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    address_line=street_address,
                    city=apartment_address,
                    country=country,
                    postal_code=zip,
                    
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('payment_view', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment_view', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order-summary")
        return render(self.request,'Alibaba/payment.html',
                      {'form':form,'order':order,
                       'shipping_address':ShippingAddress.objects.filter(user = self.request.user).first()
                                                           })    
# Payment method using paypal
class PaymentView(View):
    # get payment page with uncomplete order of logged_in user
    def get(self,request,payment_option):
        order =Order.objects.get(user=self.request.user, ordered=False)       
        if order.billing_address:
            context ={'order':
                      order,
                      'payment_option':payment_option}
            return render(request,'Alibaba/payment.html',context)
        else:
            messages.warning(self.request,"Your Order don`t have billing_address ")
            return redirect('checkout')
        
    def post(self,request,payment_option):
            order = Order.objects.get(user=self.request.user,ordered =False)
            host = request.get_host()
            invoice_id = str(uuid.uuid4()) # unique for each transaction
            paypal_dict={
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': order.total_amount_of_order(),
                'item_name': f"Order #{order.id}",
                'invoice': invoice_id,
                'currency_code': 'USD',
                'notify_url': f"http://{host}{reverse('paypal-ipn')}",
                'return_url': f"http://{host}{reverse('payment_success')}",
                'cancel_url': f"http://{host}{reverse('payment_failed')}",
            }
            paypal_form = PayPalPaymentsForm(initial = paypal_dict)
            # assign the payment to the order if payment_success to payment_success() view
            

            return render(request,'Alibaba/payment.html',{''
            'order':order,'paypal_form':paypal_form,
                })


def remove_from_cart(request, item_id):
    user=request.user
    cart_item = CartItem.objects.get(id=item_id,user=user)
    cart_item.delete()
    return redirect('viewcart')

def product_search(request):
    products = ProductModel.objects.all()
    category = request.GET.get('category')  # Use 'category' instead of 'category' for consistency
    if category:
        products = products.filter(category=category)  # Assuming 'category' is a field in your ProductModel

    return render(request, 'Alibaba/search.html', {'products': products, 'category': category})

def payment_success(request):
    order=Order.objects.get(user=request.user,ordered =False)
    order.ordered = True
    order.save()
    return render(request,'Alibaba/payment_success.html',locals())
def payment_failed(request):
    return render(request, 'Alibaba/payment_failed.html')



class BillingAddress(View):
    def get(self, request):
        form = ShippingAddressForm()
        address = ShippingAddress.objects.filter(user=request.user)
        return render(request, 'Alibaba/address.html', context={'form': form, 'address': address})

    def post(self, request):
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')  # make sure this URL name exists
        address = ShippingAddress.objects.filter(user=request.user)
        return render(request, 'Alibaba/address.html', context={'form': form, 'address': address})

# select Address for checkout    
class SelectAddress(View):
    def post(self,request):
        selected_add_id =request.POST.get('selected_address')   
        if selected_add_id:
            address = get_object_or_404(ShippingAddress,id=selected_add_id,user=request.user) 
            request.session['seleceted_id']=address.id
            return redirect('checkout')
        return redirect('address')


        
    
    

def productJson(request):    
    pass

def aboutUs(request):
    return render(request,'Alibaba/about.html')
 
def contactUs(request):
    return render(request,'Alibaba/contact.html')
