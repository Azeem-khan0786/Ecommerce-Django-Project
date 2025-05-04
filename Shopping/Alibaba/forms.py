from django import forms
from .models import ProductModel,CustomerModel,Category,ShippingAddress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from captcha.fields import ReCaptchaField 
# from captcha.widgets import ReCaptchaV2Checkbox 

PAYMENT_CHOICES = (
    ('S','stripe'),
    ('P','paypal'),
)
#Registration f
class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email',"password1","password2")
        # exclude=('username'.help_text)
        widgets={
           
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),

        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63,widget=forms.TextInput(attrs={'class':'form-control bg-smoke','placeholder':'username1'}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
# Category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model =  Category 
        fields = '__all__'   
     
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=CustomerModel
        fields= ('name','location','city', 'mobile','zipcode','state')
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'location':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'mobile':forms.NumberInput(attrs={'class':'form-control'}),
                 'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
                 'state':forms.Select(attrs={'class':'form-control'}),

                 }
        
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm password'}),
    )
                                 
                                 
# CheckOutForm            
class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Jama masjid',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'

    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('user',)