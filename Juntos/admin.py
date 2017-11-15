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

class Product_ImageInline(nested_admin.NestedStackedInline):
	model = ProductImage
	fields = ['product_images', 'product_color']
	extra = 1


class Product_colorInline(nested_admin.NestedStackedInline):
	model = ProductColor
	fields = ['color', 'product']
	list_editable = ["color", ]
	extra = 1
	inlines = [Product_ImageInline]


# from django.conf.urls.defaults import *
class Payment_methodInline(nested_admin.NestedStackedInline):
	services = forms.CharField(widget=CKEditorWidget())
	model = PaymentMethod
	fields = ['case_on_delivery', 'online_payment', 'paypal', 'product', 'services']
	extra = 1
	can_delete = False

class ProductManagementForm(forms.ModelForm):
	# feature = forms.CharField(widget=CKEditorWidget())
	description = forms.CharField(widget=CKEditorWidget())
	
	# feature     = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = ProductsManagement
		fields = ["vendor", "category", "subs_category", "title", "description", "feature", "price", "selling_price",
		          "in_stock", "product_quantity", "image", "recommended"]
	
	def __init__(self, *args, **kwargs):
		super(ProductManagementForm, self).__init__(*args, **kwargs)
		self.fields['vendor'].queryset = MyUser.objects.filter(is_vendor=True, is_active=True)


class ProductModelAdmin(nested_admin.NestedModelAdmin):
	list_display = ["category", "vendor", "subs_category", "title", "product_images", "payment_mode","price", "expire_products"]
	fields = ["vendor", "category", "subs_category", "title", "description", "feature", "price", "selling_price","in_stock", "product_quantity", "image", "recommended"]
	list_display_links = ["category"]
	list_filter = ["updated", "description"]
	search_fields = ["title", "description"]
	# inlines = [Payment_methodInline, Product_colorInline]
	# form = ProductManagementForm

	def price(self,obj):
		return obj.selling_price if obj.selling_price else obj.price
	
	def subcategory_feeds(self, request):
		from django.core import serializers
		if request.POST.get('category_id', None):
			category = request.POST['category_id']
			data = Sub_Category.objects.filter(category_id=category)
			dictionaries = [obj.as_dict() for obj in data]
			datas = json.dumps({"data": dictionaries})
			return HttpResponse(datas, content_type='application/json')
	
	def subcategory_color(self, request):
		from django.core import serializers
		if request.POST.get('subcategory_id', None):
			subcategory = request.POST['subcategory_id']
			data = Sub_Category.objects.get(id=subcategory)
			# dictionaries = [ obj.as_dict() for obj in data ]
			datas = json.dumps({"data": data.sub_category_tag})
			return HttpResponse(datas, content_type='application/json')
	
	def get_urls(self):
		from django.conf.urls import url
		urls = super(ProductModelAdmin, self).get_urls()
		my_urls = [
			url(r'subcategory_feeds', self.admin_site.admin_view(self.subcategory_feeds), name='subcategories', ),
			url(r'subcategory_color', self.admin_site.admin_view(self.subcategory_color), name='subcategory_color', ),
		]
		return my_urls + urls
	
	def product_images(self, obj):
		return mark_safe("<img src={0} style='width:35px;height:35px;'>".format(obj.image[0] if obj.image else ""))
	
	def cod_payment_avaibale(self, obj):
		if obj.payment_method:
			return obj.payment_method.case_on_delivery
		else:
			return "--empty--"
	
	def online_payment_avaibale(self, obj):
		if obj.payment_method:
			return obj.payment_method.online_payment
		else:
			return "--empty--"
	
	def get_form(self, request, obj=None, **kwargs):
		form = super(ProductModelAdmin, self).get_form(request, **kwargs)
		return form
	
	def has_add_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		else:
			return True
	
	def has_delete_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		else:
			return True
	
	def has_change_permission(self, request, obj=None):
		if request.user.is_subadmin:
			return False
		else:
			return True
	
	# def save_model(self, request, obj, form, change):
	# 	if obj.image:
	# 		if "googleusercontent.com" not in str(obj.image) and "res.cloudinary.com" not in str(
	# 				obj.image) and "fbcdn.net" not in str(obj.image):
	# 			upresult = upload(obj.image)
	# 			obj.image = upresult['url']
	# 	obj.save()
		
admin.site.register(ProductsManagement, ProductModelAdmin)