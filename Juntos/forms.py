from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import (authenticate, get_user_model, password_validation,)
from .models import *

class UserRegistration(forms.ModelForm):
    first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please Enter Valid Name.","required":"Please Enter Full Name."})
    email = forms.EmailField(required = True, error_messages = {"required":"Please Enter A Email."})
    mobile=forms.RegexField(regex=r'^\+?1?\d{9,18}$',error_messages = {"invalid":"Please Enter Valid Mobile Number.","required":"Please Enter Mobile Number."})
    password=forms.RegexField(regex=r'(?=^.{6,}$)(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9]).*',required=True,strip=False,error_messages = {"invalid":"Minimum of 8 character and a maximum of 16. Must have at least three of following:uppercase letter, lowercase letter, number(0-9)and/or special character/symbol. Password is case-sensitive","required":"Please Enter Password."})
    confirm_password=forms.CharField(required=True,strip=False,error_messages = {"required":"Please Enter Confirm Password"})

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if (len(password) < 8 or None):
            raise forms.ValidationError(("Password must be at least 8 charactors."))
            return password
        elif (len(password) > 15):
            raise forms.ValidationError(("Password must be not more than 15 charactors."))
            return password
        return self.cleaned_data.get('password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Your Confirm passwords do not match')
            return self.cleaned_data.get('password')

    def clean_first_name(self):
    	full_name = self.cleaned_data.get('first_name')
    	if len(full_name) > 40:
    		raise forms.ValidationError('Enter Only 40 charactors in Full Name')
    	return self.cleaned_data.get('first_name')

    class Meta:
    	model = MyUser
    	fields = ('first_name', 'email' ,'mobile','password','confirm_password')

class UserLoginForm(forms.Form):
   email=forms.CharField(required=True, error_messages = {"required":"Please Enter Your Email."})
   password=forms.CharField(required=True, strip=False, error_messages = {"required":"Please Enter Your Password."})

class ShippingForm(forms.ModelForm):
    billing_first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",
                                  error_messages = {"invalid":"Please Enter valid name.","required":"Please Enter your first name."})
    billing__last_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",
                                  error_messages = {"invalid":"Please Enter valid name.","required":"Please Enter your last name."})
    billing__phone=forms.RegexField(required = True, regex=r'^\+?1?\d{9,18}$',
                            error_messages = {"invalid":"The mobile number you Entered is not valid.","required":"Please Enter your phone number."})
    billing__company=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter company."})
    billing__country=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter your country."})
    billing__city=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter city."})
    billing__address=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter address."})
    billing__country_abbriviation=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter country abbriviation letters"})
    billing__state=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter state."})
    billing__zip=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter zip."})
    billing__email = forms.EmailField(required = True, error_messages = {"required":"Please Enter a email."})

    shipping_first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",
                                  error_messages = {"invalid":"Please enter valid name.","required":"Please enter your first name."})
    shipping_last_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",
                                  error_messages = {"invalid":"Please enter valid name.","required":"Please enter your last name."})
    shipping_phone=forms.RegexField(required = True, regex=r'^\+?1?\d{9,18}$',
                            error_messages = {"invalid":"The mobile number you entered is not valid.","required":"Please enter your mobile number."})
    shipping_company=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter Company."})
    shipping_country=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter Country."})
    shipping_city=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter City."})
    shipping_address=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter Address."})
    shipping_country_abbriviation=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter country Abbriviation Letters"})
    shipping_state=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter State."})
    shipping_zip=forms.CharField(required = True,
                         error_messages = {"required":"Please Enter Zipcode"})
    shipping_email = forms.EmailField(required = True, error_messages = {"required":"Please Enter A Email."})
    mode_of_transport = forms.CharField(required=False)
    