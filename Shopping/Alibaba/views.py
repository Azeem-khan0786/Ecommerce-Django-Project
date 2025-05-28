from django.shortcuts import render,redirect ,get_object_or_404
from .models import ProductModel,Category,CustomerModel,OrderItem,Order ,Address,CartItem,Cart
from django.views import View
from .forms import RegistrationForm,LoginForm,CustomerProfileForm,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy , reverse 
from django.http import JsonResponse,HttpResponse
from .forms import CheckoutForm ,AddressForm
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
        'categories': categories,

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
        # if data.not_in_stock:

        return render(request,'Alibaba/productDetail.html',{'data':data}) 

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
    # firstly create cart then add items into cart as cartItem
    cart , created = Cart.objects.get_or_create(user = request.user,is_ordered = False)
    product = ProductModel.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)
    if not created :
        cart_item.quantity += 1
        cart_item.save()
    return redirect('viewcart')

def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_ordered=False)
        cart_item = CartItem.objects.filter(cart=cart)
        amount = 0

        for item in cart_item:
            value = item.product.selling_price * item.quantity
            amount += value

        count = len(cart_item)
        total_amount = amount + 40

    except Cart.DoesNotExist:
        cart = None
        cart_item = []
        amount = 0
        count = 0
        total_amount = 0

    return render(request, 'Alibaba/cart.html', {
        'cart': cart,
        'cart_item': cart_item,
        'amount': amount,
        'count': count,
        'total_amount': total_amount
    })


# A OrderItem when goto checkout from cartItems
# def add_orderItem(request):
    # check if user already has a pending Order
    existing_order = Order.objects.filter(user= request.user,status = 'pending').first()

    if existing_order:
        return redirect('checkout',order_id = existing_order.id)
    
    cart_item =CartItem.objects.filter(user=request.user)
    if not cart_item.exists():
        return redirect('viewcart') # not item iincard 
    #  firstly create an order
    order =Order.objects.create(
        user=request.user,
        status ='pending'
    )
    for  item in cart_item:
            order_item =OrderItem.objects.create(
            order=order,
            product = item.product,
            quantity = item.quantity,
            price = item.product.selling_price
             )
    print('Order_id',order.id)        
            # order_item.save()
    return render(request,'Alibaba/checkout.html',{'order_id':order.id,'order_item':order_item})
    
class Checkout(View):
    def get(self, *args, **kwargs):
               
            order= convert_cart_to_order(self.request)
            address_id =self.request.session.get('selected_address_id') 
            if address_id:
                print('address_id ' , address_id)
                shipping_address = Address.objects.get(id=address_id,user=self.request.user)
            else:
                shipping_address = Address.objects.filter(user=self.request.user).first()
            
            # shipping_address = Address.objects.filter(user=self.request.user, address_type='shipping')
            billing_address = Address.objects.filter(user=self.request.user,address_type = 'billing').first()
            
            
            # print('order',order)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'shipping_address': shipping_address,
                'billing_address': billing_address,
            }
            return render(self.request, "Alibaba/checkout.html", context)

        # except ObjectDoesNotExist:
        #     messages.info(self.request, "You do not have an active order")
        #     return redirect("viewcart")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False).first()
            print(self.request.POST)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                # Retrieve selected shipping address from session
                address_id =self.request.session.get('selected_address_id') 
                if address_id:
                    shipping_address = Address.objects.get(id=address_id, user=self.request.user)
                else:
                    shipping_address = Address.objects.filter(user=self.request.user).first()
                if not shipping_address:
                    messages.error(self.request,'Please select a shipping address.')
                    return redirect('checkout')
                
                order.shipping_address = shipping_address
                order.status = 'Pending'
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('payment_view', payment_option='stripe')
                elif payment_option == 'P':
                    order.status ='pending'
                    order.payment_option='P'
                    order.save()
                    return redirect('payment_view', payment_option='paypal')
                elif payment_option == 'COD':
                    order.status = 'confirmed'
                    order.payment_option='COD'
                    order.ordered = True
                    order.save()
                    return redirect('get_order')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("order-summary")
        return render(self.request,'Alibaba/payment.html',
                      {'form':form,'order':order,
                    #    'shipping_address':shipping_address
                                                           })    

def convert_cart_to_order(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=False).first()

    if not cart:
        # Return the latest unplaced order if cart is already used
        existing_order = Order.objects.filter(user=request.user, ordered=False).first()
        if existing_order:
            return existing_order
        raise ValueError("No active cart or existing order.")

    if cart.is_ordered:
        if cart.order:
            return cart.order
        raise ValueError('Cart already ordered')

    cart_items = cart.cart_items.all()  # ✅ this was missing

    if not cart_items.exists():
        raise ValueError('Cannot order with an empty cart')

    # Calculate total (optional, not stored here)
    order_total = sum(cartitem.product.selling_price * cartitem.quantity for cartitem in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount = order_total + 40,  # including shipping charge
        ordered=False,
        
    )
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.selling_price
        )
    # Optional: delete cart items after moving to order

    cart.cart_items.all().delete()
    cart.is_ordered = True
    cart.order = order
    cart.save()
    return order

class OrderStatusView(View):
    def get(self,request):
            order = Order.objects.filter(user=self.request.user).latest('ordered_date')
            # Status mapping for templates
            status_info = {
                'P': {  # PayPal statuses
                    'pending': 'Waiting for payment confirmation',
                    'processing': 'Payment received, preparing order',
                    'completed': 'Order fulfilled',
                    'failed': 'Payment failed',
                    'refunded': 'Refund processed'
                },
                'COD': {  # COD statuses
                    'confirmed': 'Order confirmed',
                    'shipped': 'On the way',
                    'delivered': 'Delivered - Please pay the delivery agent',
                    'completed': 'Order complete',
                    'returned': 'Items returned'
                }
            }
            context ={'order':order,
                    'status_message': status_info[order.payment_option].get(order.status, ''),
                     'next_step' : self.get_next_step(order)
                    }

            return render(request,'Alibaba/orderstatus.html',context)
    def get_next_step(self,order):
        if order.payment_option == 'P' and order.status =='pending':
            return "Confirmed your paypal payment for proceed!"
        elif order.payment_option == 'COD' and order.status == 'confirmed':
            return 'We are shipping your order'

# Payment method using paypal
class PaymentView(View):
    # get payment page with uncomplete order of logged_in user
    def get(self, request, payment_option):
        try:
            order = Order.objects.filter(user=request.user, ordered=False).first()
        except Order.DoesNotExist:
            messages.error(request, "No active order found.")
            return redirect('cart')  # or wherever appropriate
        
        host = request.get_host()
        invoice_id = str(uuid.uuid4())  # unique invoice

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': order.total_amount_of_order(),  # Ensure this method returns Decimal
            'item_name': f"Order #{order.id}",
            'invoice': invoice_id,
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment_success')}",
            'cancel_return': f"http://{host}{reverse('payment_failed')}",
        }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        if order.shipping_address:
            context = {
                'order': order,
                'payment_option': payment_option,
                'paypal_form': paypal_form
            }
            return render(request, 'Alibaba/payment.html', context)
        else:
            messages.warning(request, "Your order doesn't have a shipping address.")
            return redirect('checkout')
        
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



class AddressView(View):
    def get(self, request):
        form = AddressForm()
        shipping_address = Address.objects.filter(
        user=request.user,
        address_type='shipping'  # Note: use the actual value stored in your DB
         )
        
        billing_address = Address.objects.filter(user=request.user,address_type = 'billing').first()
        return render(request, 'Alibaba/address.html', context={'form': form, 'shipping_address': shipping_address,'billing_address':billing_address})
    
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')  # make sure this URL name exists
        address = Address.objects.filter(user=request.user)
        return render(request, 'Alibaba/address.html', context={'form': form, 'address': address})

# select Address for checkout    
class SelectAddress(View):
    def post(self,request):
        selected_address_id =request.POST.get('shipping_address')   
        print('selected_address_id',selected_address_id)
        if selected_address_id:
            address = get_object_or_404(Address,id=selected_address_id,user=request.user) 
            request.session['selected_address_id']=address.id
            return redirect('checkout')
        return redirect('address')

def productJson(request):    
    pass

def aboutUs(request):
    return render(request,'Alibaba/about.html')
 
def contactUs(request):
    return render(request,'Alibaba/contact.html')
