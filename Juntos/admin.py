from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import nested_admin
import cloudinary
admin.site.unregister(Group)
import json
from templated_email import send_templated_mail
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
import pusher
from datetime import datetime
from .models import *
from .choices import *

# Register your models here.
admin.site.register(MyUser)

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
				sub_category_list = sub_category_list + "<option value='{0}'>{1}</option>".format(sub['id'],sub['sub_category_name'])
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


class ServicesAdmin(admin.ModelAdmin):
	list_display = ["service_type"]
	
	class Meta:
		model = Services
		fields = ["service_type"]
admin.site.register(Services, ServicesAdmin)



# class Advertisement_ImageInline(nested_admin.NestedStackedInline):
#     model = AdvertisementImage
#     fields = ['image']
#     extra = 1

# class AdvertisementForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorWidget())
    
#     class Meta:
#         model = Advertisement
#         fields = ["email", "subs_category", "type_of_services", "title", "description","name","location","price", "image","mobile","recommended"]
#     def __init__(self, *args, **kwargs):
#         super(AdvertisementForm, self).__init__(*args, **kwargs)
#         self.fields['subs_category'].queryset = SubCategory.objects.filter(sub_category_tag="VP")

class AdvertisementAdmin(nested_admin.NestedModelAdmin):
    list_display = ["email", "subs_category", "title","name", "location", "price", "description", "image"]
    # form = AdvertisementForm
    # inlines = [Advertisement_ImageInline]
    def save_model(self, request, obj, form, change):
        if obj.image:
            if "googleusercontent.com" not in str(obj.image) and "res.cloudinary.com" not in str(obj.image) and "fbcdn.net" not in str(obj.image):
                upresult = upload(obj.image)
                obj.image = upresult['url']
        obj.save()
admin.site.register(Advertisement, AdvertisementAdmin)
