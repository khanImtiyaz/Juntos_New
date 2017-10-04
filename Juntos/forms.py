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

