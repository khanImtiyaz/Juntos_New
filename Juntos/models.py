from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.signals import *
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from multiselectfield import MultiSelectField
from templated_email import send_templated_mail
from random import randrange
from datetime import datetime
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField
from colorfield.fields import ColorField
from slugify import slugify
from templated_email import send_templated_mail
import pyotp
import uuid
import string
from .choices import *
from .twillio import *



class MyUserManager(BaseUserManager):
   def create_user(self, username=None, email=None, password=None):
       """
       Creates and saves a User with the given email, and password.
       """
       user = self.model(email=self.normalize_email(email))
       user.set_password(password)
       user.save(using=self._db)
       return user

   def create_superuser(self, email, password,**kwargs):
       """
       Creates and saves a superuser with the given email and password.
       """
       user = self.create_user(email=email,password=password)
       user.is_superuser=True
       user.is_admin = True
       user.is_staff = True
       user.confirmation_code = "Confirmed"
       user.save(using=self._db)
       return user

class MyUser(AbstractBaseUser,PermissionsMixin):
  username = models.CharField(max_length=30, blank=True)
  email = models.EmailField(('email address'), max_length=255, unique=True, blank=False, error_messages={'unique':"This email has been already registered."})
  first_name = models.CharField(('first name'),max_length=50,blank=False,default='')
  last_name = models.CharField(('Last name'),max_length=50,blank=True,default='')
  avatar = CloudinaryField(null=True, blank=True, max_length=5000)
  mobile = models.CharField(('Mobile'),max_length=20,blank=True,unique=False)
  mobile_verified = models.BooleanField(('Mobile number Verified'), default=False)
  mobile_verification_code = models.CharField(('Mobile verification code'),max_length=12,blank=True, null=True)
  pincode = models.CharField(('Vendor pincode'),max_length=10,blank=True,null=True)
  city = models.CharField(('City'),max_length=50,blank=False)
  login_type = models.CharField(('Login Type'),max_length=10, default="normal")
  state = models.CharField(('State'),max_length=50,blank=True,null=True)
  country = models.CharField(('Country'),max_length=50,blank=True,null=True)
  is_superuser = models.BooleanField(('Active'),default=False)
  is_active = models.BooleanField(('Active'),default=True)
  is_admin = models.BooleanField(('Admin'),default=False)
  is_customer = models.BooleanField(('Customer'), default=False)
  is_vendor = models.BooleanField(('Vendor'), default=False)
  vendor_step = models.CharField(('Vendor Step'),max_length=50,blank=True,null=True)
  is_staff = models.BooleanField(('Admin staff flag'), default=False)
  is_subadmin = models.BooleanField(('Sub Admin'), default=False)
  created_at = models.DateTimeField(('created_at'),auto_now=True)
  updated_at = models.DateTimeField(('updated_at'),auto_now=True)
  confirmation_code = models.CharField(('confirmation_code'),max_length=50,blank=False, default="Not Confirmed")
  slug = AutoSlugField(populate_from='first_name', unique_with='created_at', unique=True, max_length=100)
  confirmed_on = models.DateTimeField(('confirmed on'), auto_now=True)
  
  objects = MyUserManager()
  USERNAME_FIELD = 'email'
  
  def __str__(self):
    return self.email
  
  def get_short_name(self):
    return self.email

  def otp_creation(self):
    totp = pyotp.TOTP("JBSWY3DPEHPK3PXP",digits=4)
    otp = totp.now()
    self.mobile_verification_code = otp
    return otp

  def otp_send(self):
    message = "Your one time password for Juntos Mobile Verification is: "+str(self.mobile_verification_code)
    send_sms(self.mobile,message)

  def successfull(self):
    message = "Your mobile number verification is successfull."
    send_sms(self.mobile,message)

  def send_mail_activation(self):
    if self.login_type == 'normal' and self.is_customer==True:
      full_name = self.first_name + self.last_name
      send_templated_mail(template_name='welcome',from_email=settings.EMAIL_HOST_USER,recipient_list=[self.email],context={'username': full_name,'email': self.email,'code': self.confirmation_code})


  class Meta:
    verbose_name_plural = ("Users")

class Banner(models.Model):
    title = models.CharField(('Banner Tag'),max_length=100, blank=True,null=True)
    description = models.CharField(('Banner Description'), max_length=500, blank=True,null=True)
    status = models.BooleanField(('Mark tick to show on banner'),default=False)
    image = CloudinaryField("Image")
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
      verbose_name = ("Banner")
      verbose_name_plural = ("Banner")


class Category(models.Model):
    category_name = models.CharField(max_length=120)
    priority = models.IntegerField(blank=True,null=True,default=1)
    icon = CloudinaryField(('Category icon'),"Image")
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.category_name
    class Meta:
        ordering = ('priority',)
        verbose_name = ('Category')
        verbose_name_plural = ("Categories")


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_category")
    sub_category_tag = models.CharField(('Subcategory tag'),max_length=120, choices=TAG,default='CP',blank=True,null=True)
    sub_category_name = models.CharField(('Sub category name'),max_length=120)
    priority = models.IntegerField(blank=True,null=True,default=1)
    subcategory_size = MultiSelectField(choices=SIZE, max_length=50, default="", null=True, blank=True)
    subcategory_shoes_size = MultiSelectField(choices=SHOES_SIZE, max_length=50, default="", null=True, blank=True)
    sub_category_flage = models.CharField(('Sub Category Flag'),max_length=10,blank=True, choices=FLAGE, null=True, help_text="Is Cloth or Shoes ?")
    slug = AutoSlugField(populate_from=['sub_category_name', 'sub_category_tag'],unique=True)
    ordering = ['priority']
    def __str__(self):
        return self.sub_category_name
    class Meta:
        verbose_name_plural = ("Product Sub Categories")
    def as_dict(self):
        return {
            "id": self.id,
            "sub_category_name": self.sub_category_name
             }

  ###It is important at this place please don't change it postition

class ProductsManagement(models.Model):
  vendor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="vendor_product")
  product_sku = models.CharField("Product ID", max_length=50, blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cat_product")
  subs_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, related_name="sub_cat_product")
  title = models.CharField('Product Title', max_length=200)
  description = models.TextField('Product Description', blank=True)
  feature = models.TextField('Product Features', blank=True, null=True, default="Not a feature product")
  price = models.FloatField('Product Orignal Price', blank=False)
  selling_price = models.FloatField('Product Selling Price', blank=True,null=True)
  product_quantity = models.IntegerField('Product Available Quantity',default=0)
  product_rating = models.IntegerField('Product Rating', default=0,blank=True)
  image = ArrayField(models.ImageField('Product image'),null=True,blank=False)
  product_tag = models.CharField('Product Tag', max_length=300, blank=True)
  recommended = models.BooleanField('Mark as Recommended', default=False)
  slug = AutoSlugField(populate_from='subs_category', unique_with='title', unique=True, max_length=100)
  in_stock = models.BooleanField('Available', default=True)
  insured_amount = models.FloatField('Insured Amount', blank=False)
  product_weight = models.FloatField('Product Weight', blank=False)
  product_height = models.FloatField('product_height', blank=False)
  product_depth = models.FloatField('Product depth', blank=False)
  product_width = models.FloatField('Product Width', blank=False)
  payment_mode = ArrayField(models.CharField('Payment Mode', max_length=50, blank=False))
  expire_products = models.IntegerField('Expired Products', blank=True, default=15, null=True)
  services = models.TextField('Services', blank=False,default='')
  updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title

  def __unicode__(self):
    return self.title

  class Meta:
    verbose_name_plural = ("Products")

  def date_check(self):
    d1  = self.created_at
    dat = d1.date()
    d2  = datetime.now().date()
    return ((d2-dat).days)

from .signals import * 


class Notifications(models.Model):
    vendor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="nofify_vendor")
    ntype = models.CharField(('Notification Type'), max_length=200, blank=True, choices=NTYPE)
    content  = models.CharField(('Notification content'), max_length=200, blank=True)
    is_read  = models.BooleanField(('Is read ?'), default=False)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
  """add to cart """
  user =  models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cart_user')
  product = models.ForeignKey(ProductsManagement, on_delete=models.CASCADE, related_name="cart_product")
  product_color = models.IntegerField(null=True,blank=True)
  product_size = models.IntegerField(null=True,blank=True)
  quantity = models.IntegerField(('product quantity'), blank=False)
  price = models.FloatField(('total price'))
  active = models.BooleanField(default=True)
  updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now=True)


class Wishlist(models.Model):
    user =  models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='whislist')
    product = models.ForeignKey(ProductsManagement, on_delete=models.CASCADE, related_name="whislist_product")
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)


class CustomerReview(models.Model):
    """ Customer review to be desplay"""
    product = models.ForeignKey(ProductsManagement, on_delete=models.CASCADE, related_name="product_review")
    content = models.CharField(('Customer Reviews'), blank=True, max_length=100)
    rating = models.IntegerField(('Rating value'), blank=True, default=0)
    user     = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="customer_reviews")
    updated    = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Customer Reviews'



class ShippingAddress(models.Model):
  user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True,related_name="shiping_address")
  shipping_first_name =  models.CharField(('Shipping First Name'),max_length=50,blank=False, default='')
  shipping_last_name  =  models.CharField(('Shipping Last Name'),max_length=50,blank=False, default='')
  shipping_phone      =  models.CharField(('Billing Phone'),max_length=15,null=False, blank=False)
  shipping_company    =  models.CharField(('Shipping Company'),max_length=50,blank=False, default='')
  shipping_country    = models.CharField(('Shipping Country'),max_length=50, blank=False, default='')
  shipping_country_abbreviation  = models.CharField(('Shipping Country Abbreviation'),max_length=50, blank=False, default='')
  shipping_state      =  models.CharField(('Shipping State'),max_length=50,blank=False, default='')
  shipping_city       =  models.CharField(('Shipping City'),max_length=50,blank=False, default='')
  shipping_zip        =  models.CharField(('Shipping Zip'),max_length=50,blank=False, default='')
  shipping_address    =  models.CharField(('Shipping Address'),max_length=50,blank=False, default='')
  shipping_phone      =  models.CharField(('Shipping Phone'),max_length=15,null=False, blank=False)
  shipping_email      =  models.CharField(('Shipping Email'),max_length=50,blank=False, default='')
  mode_of_transport  =  models.CharField(('Mode of Transport'),max_length=50,blank=True, default='')
  selected = models.BooleanField(('Select Shipping Address'),default=False)
  created_at = models.DateTimeField(('created_at'), auto_now = True)
  updated_at = models.DateTimeField(('updated_at'), auto_now = True)

  def __str__(self):
    return self.shipping_address+", "+ str(self.shipping_zip)+", "+self.shipping_city
  class Meta:
    verbose_name_plural = 'Customer Shipping Address'

  def details(self):
    return (self.shipping_first_name+" ,"+self.shipping_address+" ,"+self.shipping_city+" ,"+self.shipping_state+" ,"+self.shipping_phone+" ,"+self.shipping_country)

class BillingAddress(models.Model):
  """docstring for BillingAddress"""
  user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True,related_name="billing_address")
  billing_first_name =  models.CharField(('Billing First Name'),max_length=50,blank=False, default='')
  billing_last_name  =  models.CharField(('Billing Last Name'),max_length=50,blank=False, default='')
  billing_company    =  models.CharField(('Billing Company'),max_length=50,blank=False, default='')
  billing_country    = models.CharField(('Billing Country'),max_length=50, blank=False, default='')
  billing_country_abbreviation  = models.CharField(('Billing Country Abbreviation'),max_length=50, blank=False, default='')
  billing_state      =  models.CharField(('Billing State'),max_length=50,blank=False, default='')
  billing_city       =  models.CharField(('Billing City'),max_length=50,blank=False, default='')
  billing_zip        =  models.CharField(('Billing Zip'),max_length=50,blank=False, default='')
  billing_address    =  models.CharField(('Billing Address'),max_length=50,blank=False, default='')
  billing_email      =  models.CharField(('Billing Email'),max_length=50,blank=False, default='')
  mode_of_transport  =  models.CharField(('Mode of Transport'),max_length=50,blank=True, default='')
  selected = models.BooleanField(('Select Shipping Address'),default=False)
  created_at = models.DateTimeField(('created_at'), auto_now = True)
  updated_at = models.DateTimeField(('updated_at'), auto_now = True)