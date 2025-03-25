from django.shortcuts import render,redirect
from .models import ProductModel,Category,CustomerModel,CartItemModel
from django.views import View
from .forms import RegistrationForm,LoginForm,CustomerProfileForm,ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy , reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # unique user_id for duplicate user


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
    data={
        'products': products,
        'categories': categories
    }

    return render(request,'Alibaba/home.html', data )

def aboutUs(request):
    return render(request,'Alibaba/about.html')
 
def contactUs(request):
    return render(request,'Alibaba/contact.html')
ChangePasswordForm
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
    
class ProductView(View):
    def get(self,request,pk):
        data=ProductModel.objects.get(id=pk)
        return render(request,'Alibaba/productDetail.html',locals())    

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

def address(request):
    add=CustomerModel.objects.filter(user=request.user)
    print(add)
    return render(request,'Alibaba/address.html',context={'add':add})
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
    cart_item, created = CartItemModel.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    # print(cart_item.quantity)
    cart_item.save()
    return redirect('viewcart')

def view_cart(request):
    cart_item = CartItemModel.objects.filter(user=request.user)
    amount = 0
    
    for item in cart_item:
        value = item.product.selling_price * item.quantity
        amount += value
    count=len(cart_item)
    total_amount = amount + 40
    
    return render(request, 'Alibaba/cart.html',locals())
    
class Checkout(View):
    def get(self,request):
        cart_item=ProductModel.objects.filter(user=request.user)
        add=CustomerModel.objects.filter(user=request.user)
        # client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
        # data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
        # payment = client.order.create(data=data)
        # get the host
        # create paypal form
        host = request.get_host()
        # dict
        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount' : 500,
            'item_name' : 'Book',
            'no_shipping':'2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'https://{}{}'.format(host,reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host,reverse("payment_success")),
            'cancel_url': 'https://{}{}'.format(host,reverse("payment_failed")),


        }
        paypal_form = PayPalPaymentsForm(initial = paypal_dict)
        return render(request,'Alibaba/checkout.html',locals())

def remove_from_cart(request, item_id):
    user=request.user
    cart_item = CartItemModel.objects.get(id=item_id,user=user)
    cart_item.delete()
    return redirect('viewcart')

def product_search(request):
    products = ProductModel.objects.all()
    category = request.GET.get('category')  # Use 'category' instead of 'category' for consistency
    if category:
        products = products.filter(category=category)  # Assuming 'category' is a field in your ProductModel

    return render(request, 'Alibaba/search.html', {'products': products, 'category': category})

def payment_success(request):
    pass
def payment_failed(request):
    pass
