from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from Juntos.choices import *
from Juntos.models import MyUser , ProductsManagement
from .models import *



class VendorRegistrationForm1(forms.ModelForm):
    city = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{3,50}$",
                               error_messages = {"invalid":"Please Enter Valid City Name.","required":"Please Enter City Name."})
    state = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{3,50}$",
                               error_messages = {"invalid":"Please Enter Valid State Name.","required":"Please Enter State Name."})
    country = forms.RegexField(required = True,  regex = "^[A-Za-z\s]{3,50}$",
                               error_messages = {"invalid":"Please Enter Valid Country Name.","required":"Please Enter Country Name."})
    agree_terms_condition = forms.BooleanField(required = True, error_messages = {"required":"Please check Term & Condition."})
    pincode = forms.CharField(required = True, error_messages = {"required":"Please Enter Pincode."})
    class Meta:
        model = MyUser
        fields = ("city","state","country","pincode")
    

class VendorRegistrationForm2(forms.ModelForm):
    business_name = forms.RegexField(required = True,  regex = "^[A-Za-z0-9\s]{4,50}$",
                               error_messages = {"invalid":"Please Enter Valid Business Name.","required":"Please Enter Business Name."})
    legal_name =forms.CharField(required = True,widget=forms.TextInput, error_messages = {"required":"Please Enter legal name."})
    class Meta:
        model = Vendor_Account_Details
        fields = ("business_name","legal_name","address1","address2")

class VendorRegistrationForm3(forms.Form):
    account_number = forms.RegexField(required = True,  regex = "^[0-9]{10,16}$",
                               error_messages = {"invalid":"Please Enter Valid Account Number.","required":"Please Enter account number."})
    routing_number = forms.RegexField(required = True,  regex = "^[0-9]{9}$",
                               error_messages = {"invalid":"Please Enter Valid ( digit Routing Code.","required":"Please Enter Routing Code."})

class NewProductAddForm(forms.ModelForm):
    price = forms.RegexField(required = True,regex = "^[0-9]",error_messages={"invalid":"Please enter Valid Price.","required":"Please enter Price for the Product"})
    selling_price = forms.FloatField(required = False,error_messages={"invalid":"Please Enter Valid Selling Price.","required":"Please enter Selling Price"})
    product_quantity = forms.RegexField(required = True,regex = "^[0-9]{1,10}$", error_messages={'invalid':"Please enter valid quantity.",'required':'Please fill quantity'})
    def clean(self):
        price = self.cleaned_data.get('price')
        selling_price = self.cleaned_data.get('selling_price')
        if price and selling_price and float(price)<float(selling_price):
            raise forms.ValidationError({'selling_price':'Selling Price not more than Product price'})

    class Meta:
        model = ProductsManagement
        exclude = ('image',)

class ProfileVendorForm(forms.Form):
    legal_name =forms.CharField(required = True,widget=forms.TextInput, error_messages = {"required":"Please Enter legal name."})
    #agree_terms_condition = forms.CharField(required = True, error_messages = {"required":"Please agree on term and condition."})
    # password=forms.RegexField(regex=r'(?=^.{6,}$)(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9]).*', required=False, strip=False, error_messages = {"invalid":"Please Enter Password and Submit 8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character", "required":"Please Enter Password."})
    # confirm_password=forms.CharField(required=False, strip=False, error_messages = {"required":"Please Enter Confirm Password"})
    business_name = forms.RegexField(required=True,  regex = "^[A-Za-z\s]{4,20}$",error_messages={"invalid":"Please Enter Valid Business Name.","required":"Please Enter Business Name."})
    pincode = forms.CharField(required=True, error_messages = {"required":"Please Enter Pincode."})
    city = forms.RegexField(required=True,  regex = "^[A-Za-z\s]{3,10}$",error_messages={"invalid":"Please Enter Valid City Name.","required":"Please Enter City Name."})
    address1 = forms.CharField(required=True, error_messages = {"required":"Please Enter address line 1"})
    address2 = forms.CharField(required=False, error_messages = {"required":"Please Enter address line 2"})
    bank_name = forms.RegexField(required=False,  regex = "^[A-Za-z0-9\s]{2,50}$",error_messages={"invalid":"Please Enter Valid Bank Name",})
    account_number = forms.RegexField(required=False,  regex = "^[0-9]{10,16}$",error_messages={"invalid":"Please Enter Valid Account Number.","required":"Please Enter account number."})
    routing_number = forms.RegexField(required=False,  regex = "^[A-Za-z0-9]{9}$",error_messages={"invalid":"Please Enter valid routing number.","required":"Please Enter routing number."})
    def clean(self):
        if self.cleaned_data.get('email',None):
            email = self.cleaned_data['email']
            user = MyUser.objects.filter(email=email)
            if user.exists():
                return self.cleaned_data
            else:
                raise forms.ValidationError({'email':'User with this email not exists.'})

import json
class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(required=True, strip=False, error_messages = {"required":"Please Enter Password"})
    new_password=forms.RegexField(regex=r'(?=^.{6,30}$)|(?=.*[0-9])|(?=.*[A-Z])|(?=.*[a-z])|(?=.*[^A-Za-z0-9]).*',required=True,strip=False,error_messages = {"invalid":"Minimum of 8 character and a maximum of 16. Must have at least three of following:uppercase letter, lowercase letter, number(0-9)and/or special character/symbol. Password is case-sensitive"})
    confirm_password=forms.CharField(required=True, strip=False, error_messages = {"required":"Please Enter Confirm Password"})

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        print('old password',self.cleaned_data.get('password'))
        if not self.user.check_password(self.cleaned_data.get('password')):
            raise forms.ValidationError({'password':'Current Password do not match.'})
        else:
            if self.cleaned_data.get('confirm_password', None) != self.cleaned_data.get('new_password', None):
                raise forms.ValidationError({'confirm_password':'New password and confirm password not matches.'})

    class Meta:
        model = MyUser
        fields = ['password','new_password','confirm_password']
