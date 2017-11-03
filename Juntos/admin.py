from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
# from django.contrib.sites.models import Site
# from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import nested_admin
import cloudinary
admin.site.unregister(Group)
# admin.site.unregister(Site)
import json
from templated_email import send_templated_mail
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
import pusher
from datetime import datetime
from .models import *
from .choices import *

# Register your models here.

class BannerForm(forms.ModelForm):
	description = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Banner
		fields = ["title", "description", "status", "image"]

class BannerModelAdmin(admin.ModelAdmin):
	list_display = ["title", "banner_description", "created_at", "banner_image"]
	form = BannerForm
	
	def banner_image(self, obj):
		return mark_safe("<img src='{0}' id='banner_image_id' style='width:105px;height:85px;'>".format(obj.image.url))
	
	def banner_description(self, obj):
		return mark_safe(obj.description)
	
admin.site.register(Banner,BannerModelAdmin)


class SubCategoryForm(forms.ModelForm):
	class Meta:
		model = SubCategory
		fields = ['sub_category_tag', 'sub_category_name', 'priority', 'sub_category_flage', 'subcategory_size',
		          'subcategory_shoes_size', 'category']
	
	def __init__(self, *args, **kwargs):
		super(SubCategoryForm, self).__init__(*args, **kwargs)
		self.fields['subcategory_size'].widget = forms.CheckboxSelectMultiple(choices=SIZE,
		                                                                      attrs={'style': 'display:initial'})
		self.fields['subcategory_shoes_size'].widget = forms.CheckboxSelectMultiple(choices=SHOES_SIZE,
		                                                                            attrs={'style': 'display:initial',
		                                                                                   'label': "Shoes Size"})
class SubCategoryInlines(admin.TabularInline):
	model = SubCategory
	form = SubCategoryForm
	extra = 0


class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ["category_name", "get_subcategory"]
	list_display_links = ["category_name"]
	list_filter = ['category_name']
	inlines = [SubCategoryInlines]
	
	def get_subcategory(self, obj):
		if obj.sub_category.exists():
			sub_category_list = "<select><option value=''>List Subcategory</option>"
			for sub in obj.sub_category.values():
				sub_category_list = sub_category_list + "<option value='{0}'>{1}</option>".format(sub['id'],
				                                                                                  sub['sub_category_name'])
			sub_category_list = sub_category_list + "</select>"
		else:
			sub_category_list = "No sub category available"
		return mark_safe(sub_category_list)
	
	get_subcategory.short_description = 'Subcategory'
	get_subcategory.admin_order_field = 'sub_category'
	
	def has_add_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		return True
	
	def has_delete_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		return True
	
	def has_change_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		return True
	
	class Meta:
		model = Category


admin.site.register(Category, CategoryModelAdmin)
class OfferAdmin(admin.ModelAdmin):
	list_display = ["product", "offer_title","offer_details", "offer_start_date_time","offer_end_date_time", "offer_price"]

	class Meta:
		model = Offer

admin.site.register(Offer,OfferAdmin)