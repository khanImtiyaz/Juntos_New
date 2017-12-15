from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import (authenticate, get_user_model, password_validation,)
from .models import *
from Static_Model.models import  SubscribeNewsLetter

class UserRegistration(forms.ModelForm):
    first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please Enter Valid Name.","required":"Please Enter Full Name."})
    email = forms.EmailField(required = True, error_messages = {"required":"Please Enter A Email."})
    mobile=forms.RegexField(regex=r'^\+?1?\d{9,18}$',error_messages = {"invalid":"Please Enter Valid Mobile Number.","required":"Please Enter Mobile Number."})
    password=forms.RegexField(regex=r'(?=^.{6,}$)|(?=.*[0-9])|(?=.*[A-Z])|(?=.*[a-z])|(?=.*[^A-Za-z0-9]).*',required=True,strip=False,error_messages = {"invalid":"*Mínimo de 8 caracteres y un máximo de 16. Debe de tener al menos 3 de los siguientes: letra mayúscula, letra minúscula, numero(0-9)y/o caracter especial/símbolo. Contraseña es sensible a mayúsculas y minúsculas.","required":"Please Enter Password."})
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

class BillingForm(forms.ModelForm):
    billing_first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please Enter valid name.","required":"Please enter your first name."})
    billing_last_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please Enter valid name.","required":"Please enter your last name."})
    billing_phone=forms.RegexField(required = True, regex=r'^\+?1?\d{9,18}$',error_messages = {"invalid":"The mobile number you Entered is not valid.","required":"Please enter your phone number."})
    billing_company=forms.CharField(required = True,error_messages = {"required":"Please enter company."})
    billing_country=forms.CharField(required = True,error_messages = {"required":"Please enter your country."})
    billing_city=forms.CharField(required = True,error_messages = {"required":"Please enter city."})
    billing_address=forms.CharField(required = True,error_messages = {"required":"Please enter address."})
    billing_country_abbreviation=forms.CharField(required = True,error_messages = {"required":"Please enter country abbreviations letters"})
    billing_state=forms.CharField(required = True,error_messages = {"required":"Please enter state."})
    billing_zip=forms.CharField(required = True,error_messages = {"required":"Please enter zip."})
    billing_email = forms.EmailField(required = True, error_messages = {"required":"Please enter email."})
    mode_of_transport = forms.CharField(required=False)

    class Meta:
        model = BillingAddress
        fields = "__all__"


class ShippingForm(forms.ModelForm):
    shipping_first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please enter valid name.","required":"Please enter your first name."})
    shipping_last_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please enter valid name.","required":"Please enter your last name."})
    shipping_phone=forms.RegexField(required = True, regex=r'^\+?1?\d{9,18}$',error_messages = {"invalid":"The mobile number you entered is not valid.","required":"Please enter your mobile number."})
    shipping_company=forms.CharField(required = True,error_messages = {"required":"Please enter Company."})
    shipping_country=forms.CharField(required = True,error_messages = {"required":"Please enter Country."})
    shipping_city=forms.CharField(required = True,error_messages = {"required":"Please enter City."})
    shipping_address=forms.CharField(required = True,error_messages = {"required":"Please enter Address."})
    shipping_country_abbreviation=forms.CharField(required = True,error_messages = {"required":"Please enter country abbreviations Letters"})
    shipping_state=forms.CharField(required = True,error_messages = {"required":"Please enter State."})
    shipping_zip=forms.CharField(required = True,error_messages = {"required":"Please enter Zipcode"})
    shipping_email = forms.EmailField(required = True, error_messages = {"required":"Please enter email."})
    mode_of_transport = forms.CharField(required=False)

    class Meta:
        model = ShippingAddress
        fields = "__all__"

class ProfileForm(forms.Form):
    first_name = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$",error_messages = {"invalid":"Please Enter Valid Name.","required":"Please Enter Name."})
    mobile=forms.RegexField(regex=r'^\+?1?\d{9,18}$',error_messages = {"invalid":"Please Enter Valid Mobile Number.","required":"Please Enter Mobile Number."})


class JuntosContactUsEmailForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = JuntosContactUsEmail
    #     fields = "__all__"

class SubscribeNewsLetterForm(forms.ModelForm):
    class Meta:
        model = SubscribeNewsLetter
        fields = "__all__"

    