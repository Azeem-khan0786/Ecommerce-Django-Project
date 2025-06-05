from django import forms
from .models import ProductModel,ProfileModel,Category,Address
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget 

PAYMENT_CHOICES = (
    ('S','stripe'),
    ('P','paypal'),
    ('COD','Cash on Delivery'),
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

class CategoryForm(forms.ModelForm):
    class Meta:
        model =  Category 
        fields = '__all__'   
     

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = (
            'name',
            'mobile',
            'date_of_birth',
            'gender',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'zipcode',
            'country',
            'profile_picture',
        )

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Full Name'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Mobile Number (e.g. +91-9876543210)'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Address Line 1'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Address Line 2 (Optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ZIP / Postal Code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Country'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-file'
            }),
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

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user',)

