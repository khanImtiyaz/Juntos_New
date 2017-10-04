from django.db import models
from Juntos.models import MyUser
from .choices import *

class Vendor_Account_Details(models.Model):
    vendor = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, related_name='account')
    legal_name = models.CharField('Legal name', max_length=30,blank=False, null=False)
    business_name = models.CharField('Business name', max_length=20, blank=False, null=False)
    business_url = models.CharField('Business Url', max_length=50, blank=True, null=True, help_text="Ex: http://peru.com")
    agree_terms_condition = models.BooleanField('Agree Term & condition', default=False, blank=True, help_text="Clicking on this you are supposed to agree terms and condition of Peru Juntos")
    bank_name = models.CharField('Bank Name', max_length=30, blank=False, null=False)
    account_number = models.CharField('Account Number', max_length=16, blank=False, null=False)
    routing_number = models.CharField('Routing Number', max_length=20, blank=False, null=False)
    address1 = models.TextField('Address line 1', max_length=100, blank=False, default='')
    address2 = models.TextField('Address line 2', max_length=100, blank=True, default='')
    gender = models.CharField("Gender", max_length=10, null=True, choices=GENDER)
    created_at = models.DateTimeField('created_at', auto_now=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    def __str__(self):
        return str(self.legal_name)
        
    class Meta:
        verbose_name_plural = "Vendor Account Details"