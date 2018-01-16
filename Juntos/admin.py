from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin import SimpleListFilter
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django import forms
from ckeditor.widgets import CKEditorWidget
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import nested_admin
import cloudinary
from cloudinary.uploader import upload, upload_resource
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

	class Media:
		js = (
			'js/subCategory.js',
		)


class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ["category_name","priority"]
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



admin.site.register(TaxPercentage)



class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    fields = ['image']
    extra = 0


class AdvertisementForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Advertisement
        fields = ["title", "type_of_services","description","price","name","email","mobile","location","recommended","valid_upto"]

    # def __init__(self, *args, **kwargs):
    #     super(AdvertisementForm, self).__init__(*args, **kwargs)
    #     self.fields['subs_category'].queryset = SubCategory.objects.filter(sub_category_tag="VP")


class AdvertisementAdmin(admin.ModelAdmin):
	list_display = ["name", "email","title","description","price","valid_upto"]
	inlines = [AdvertisementImageInline]
	form = AdvertisementForm
admin.site.register(Advertisement, AdvertisementAdmin)

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	fields = ['product_images', 'product_color']
	extra = 0


class Product_colorInline(admin.TabularInline):
	model = ProductColor
	fields = ['color', 'product']
	list_editable = ["color", ]
	extra = 0
	inlines = [ProductImageInline]


# from django.conf.urls.defaults import *
class Payment_methodInline(nested_admin.NestedStackedInline):
	services = forms.CharField(widget=CKEditorWidget())
	model = PaymentMethod
	fields = ['case_on_delivery', 'online_payment', 'paypal', 'product', 'services']
	extra = 0
	can_delete = True

# class ProductManagementForm(forms.ModelForm):
# 	# feature = forms.CharField(widget=CKEditorWidget())
# 	description = forms.CharField(widget=CKEditorWidget())
	
# 	# feature     = forms.CharField(widget=CKEditorWidget())
# 	class Meta:
# 		model = ProductsManagement
# 		fields = ["vendor", "category", "subs_category", "title", "description", "feature", "price", "selling_price",
# 		          "in_stock", "product_quantity", "image", "recommended"]
	
# 	def __init__(self, *args, **kwargs):
# 		super(ProductManagementForm, self).__init__(*args, **kwargs)
# 		self.fields['vendor'].queryset = MyUser.objects.filter(is_vendor=True, is_active=True)


class ProductModelAdmin(nested_admin.NestedModelAdmin):
	list_display = ("title", "vendor", "category", "subs_category", "product_images", "payment_mode","price", "expiry_date")
	fields = ("vendor", "category", "subs_category", "title", "description", "feature", "price", "selling_price","in_stock", "product_quantity", "image", "recommended")
	list_filter = ["updated", "description"]
	search_fields = ["title", "description"]
	readonly_fields = ('image',)
	# inlines = [Product_colorInline]
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
		return True
	
	def has_delete_permission(self, request, obj=None):
		return True
	
	def has_change_permission(self, request, obj=None):
		return True
	
	# def save_model(self, request, obj, form, change):
	# 	if obj.image:
	# 		if "googleusercontent.com" not in str(obj.image) and "res.cloudinary.com" not in str(
	# 				obj.image) and "fbcdn.net" not in str(obj.image):
	# 			upresult = upload(obj.image)
	# 			obj.image = upresult['url']
	# 	obj.save()
		
admin.site.register(ProductsManagement, ProductModelAdmin)


class NewsModelAdmin(admin.ModelAdmin):
	list_display = ["title", "created_at"]

	class Meta:
		model = News

admin.site.register(News, NewsModelAdmin)



class CustomerFilter(SimpleListFilter):
	title = ('Customer')
	parameter_name = 'customer'
	
	def lookups(self, request, model_admin):
		list_tuple = []
		for client in MyUser.objects.filter(is_customer=True):
			list_tuple.append((client.id, client.email))
		return list_tuple
	
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(customer__id=self.value())
		else:
			return queryset



class CustomerOrderAdmin(admin.ModelAdmin):
	list_display = ['shipping_address','customer','order_payment_type','order_items','order_number','delivery_date','delivery_status','expected_delivery','total','order_date_and_time']
	search_fields = ['order_number', 'customer__email', 'delivery_date']
	list_filter = [CustomerFilter, 'delivery_status']
	list_per_page = 15
	
	def get_search_results(self, request, queryset, search_term):
		from django.contrib import messages
		queryset, use_distinct = super(CustomerOrderAdmin, self).get_search_results(request, queryset, search_term)
		if not queryset.count():
			messages.info(request, 'No order data found !')
		return queryset, use_distinct
	
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
	
	def order_date_and_time(self, obj):
		return obj.created_at
	
	def expected_delivery(self, obj):
		return str(obj.expected_delivery_time) + str(" days")
	
	def order_items(self, obj):
		obj.order_items.all()
		return
	
	def order_items(self, obj):
		items_list = "<select><option value=''>List Order Items</option>"
		for sub in obj.order_items.all():
			items_list = items_list + "<option value='{0}'>{1}</option>".format(sub.id, sub.product.title)
		items_list = items_list + "</select>"
		
		return mark_safe(items_list)

admin.site.register(CustomerOrder,CustomerOrderAdmin)