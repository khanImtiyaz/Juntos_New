from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from slugify import slugify
from .models import *

   
# Signals
@receiver(pre_save, sender=SubCategory)
def model_pre_save_SubCategory(sender, **kwargs):
	data = kwargs['instance']
	kwargs['instance'].slug = slugify(data['sub_category_name']+str(data['id']))


@receiver(pre_save, sender=ProductsManagement)
def model_pre_save_ProductsManagement(sender, **kwargs):
	data = kwargs['instance']
	kwargs['instance'].slug = slugify(data.title+str(data.subs_category)+str(data.id))
