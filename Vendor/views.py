# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.contrib.auth import update_session_auth_hash 
from django.db.models import Count,Sum
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from cloudinary.uploader import upload, upload_resource
import os
import base64
from base64 import b64encode
import json
from Juntos.models import *
from itertools import groupby
import operator
from Django_Multiple.utils import *
from .forms import *

# Create your views here.
class VendorSignup(View):
	"""docstring for VendorSignup"""
	def get(self,request):
		user = request.user
		if not user.vendor_step:
			return render(request, 'vendor/registration_form1.html')
		elif user.vendor_step=="Step1":
			return render(request, 'vendor/registration_form2.html')
		elif user.vendor_step=="Step2":
			return render(request, 'vendor/registration_form3.html')
		else:
			return render(request, 'vendor/registration_form1.html')



class VendorSignupStep1(View):
	"""docstring for VendorSignupStep1"""
	def post(self,request):
		queryset = MyUser.objects.all()
		params = request.POST
		user = request.user
		form = VendorRegistrationForm1(params or None, instance=user)
		if form.is_valid():
			form.save()
			if request.FILES.get('avatar', None):
				upresult = upload(request.FILES['avatar'])
				user.avatar = upresult
				user.is_vendor = True
				user.is_customer = True
				user.vendor_step ="Step1"
				user.save()
				return render(request, 'vendor/registration_form2.html')
		else:
			return render(request, 'vendor/registration_form1.html', {'vendor': form})
		
class VendorSignupStep2(View):
	"""docstring for VendorSignupStep2"""
	def post(self,request):
		queryset = MyUser.objects.all()
		params = request.POST
		user = request.user
		form = VendorRegistrationForm2(params or None)
		if form.is_valid():
			request.session['business_name'] = params['business_name']
			request.session['legal_name']    = params['legal_name']
			request.session['address1']      = params['address1']
			request.session['address2']      = params['address2']
			messages.success(request, 'Seller business information saved.')
			return render(request, 'vendor/registration_form3.html')
		else:
			return render(request, 'vendor/registration_form2.html', {'vendor': form})

class VendorSignupStep3(View):
	"""docstring for VendorSignupStep3"""
	def post(self,request):
		queryset = MyUser.objects.all()
		params = request.POST
		user = request.user
		form = VendorRegistrationForm3(params or None)
		if form.is_valid():
			bank = Vendor_Account_Details.objects.create(vendor=user,
				bank_name=params['bank_name'],
				routing_number=params['routing_number'],
				account_number=params['account_number'],
				agree_terms_condition=True,
				address1=request.session['address1'],
				address2=request.session['address2'],
				legal_name=request.session['legal_name'],
				business_name=request.session['business_name']
			)
			user.vendor_step ="Step3"
			user.is_vendor = True
			user.save()
			messages.info(request, 'Signing up success.')
			return redirect('Vendor:vendor-dashboard')
		else:
			return render(request, 'vendor/registration_form3.html', {'vendor': form})

class BVendor(View):
	"""docstring for BVendor"""
	def get(self,request):
		return redirect('Juntos:home')


class VendorDashboard(View):
	"""docstring for VendorDashboard"""
	def get(self,request):
		vendor = request.user
		if not vendor.is_vendor or not vendor.is_active:
			messages.error(request, "You are not authorize to access this page.")
			return redirect('Juntos:home')
		else:
			orders = OrderItems.objects.filter(product__vendor=vendor).order_by('-created_at')
			total_sell = orders.aggregate(Sum('total'))['total__sum'] if orders.aggregate(Sum('total'))['total__sum'] else  00.00
			products = ProductsManagement.objects.filter(vendor=vendor)
			orderHash = []
			typeArray = [['Year', 'Sales', 'Expenses', 'Profit']]
			orders = orders.filter(created_at__month=datetime.today().month)
			for product in products:
				if product.order.exists():
					orderList = product.order.filter(created_at__month=datetime.today().month)
					for order in orderList:
						if not any( orderl.get('id') == order.product.id for orderl in orderHash):
							sales = orderList.filter(product_id=order.product.id).aggregate(Sum('base_price'))['base_price__sum']
							total_original_price = orderList.filter(product_id=order.product.id).count() * order.product.price
							total_expenses_price = product.price*product.product_quantity
							orderHash.append({"title":order.product.title, "sales":sales,"profit":sales-total_original_price,"expenses":sales-total_expenses_price})
				else:
					orderHash.append({"title":product.title, "sales":00.00,"profit":00.00,"expenses":product.price*product.product_quantity})
			if orderHash:
				for record in orderHash:
					typeArray.append([str(record['title']),record['sales'],record['expenses'],record['profit']])

			return render(request, 'vendor/dashboard.html',{'orders':orders,"total_sell":total_sell,"sell_hash": typeArray,})
	

class LogoutView(View):
	"""docstring for LogoutView"""
	def get(self,request):
		logout(request)
		return redirect("Vendor:bevendor")

class ChangePassword(View):
	"""docstring for ChangePassword"""
	def post(self,request):
		form = ChangePasswordForm(request.POST, user=request.user)
		if form.is_valid():
			user = request.user
			check = user.check_password(request.POST.get('password'))
			if check:
				user.set_password(request.POST.get('new_password', user.password))
				user.save()
				update_session_auth_hash(request, form.user)
			else:
				messages.error(request, "Current Password do not match.")
				return render(request,'vendor/change_password.html',{"forms":form})
			messages.success(request, "Password changed successfully.")
			return redirect("Vendor:vendor-dashboard")
		else:
			return render(request,'vendor/change_password.html',{"forms":form})

	def get(self,request):
		return render(request,'vendor/change_password.html')


	
class OrderHistory(View):
	"""docstring for OrderHistory"""
	def get(self,request,status):
		orders = OrderItems.objects.filter(product__vendor=request.user,delivery_status=status).order_by('-created_at')
		return render(request, 'vendor/order-history.html',{'orders':orders})

class OrderDelivered(View):
	"""docstring for OrderHistory"""
	def get(self,request,pk=None):
		order = OrderItems.objects.get(id=pk)
		order.delivery_status = "Delivered"
		order.order.delivery_status = True
		order.order.save()
		order.save()
		return redirect("Vendor:orders-history", "Pending")

def add_product(request):

    if request.method == "POST":
        category = Category.objects.all()
        form = NewProductAddForm(request.POST, None)
        if form.is_valid():
            params = request.POST
            if product:
                product.vendor = request.user;
                product.title=params['title']
                product.description = params['description']
                product.price = float(params['price'])
                product.selling_price = params['selling_price']
                product.category_id=params['category']
                product.subs_category_id = params['subs_category']
                product.product_quantity = params['product_quantity']
                product.insured_amount = params['insured_amount']
                product.product_weight = params['product_weight']
                product.product_height = params['product_height']
                product.product_depth = params['product_depth']
                product.product_width = params['product_width']
                # product.save()
            else:
                product = Products_Management(
                    vendor = request.user,
                    title=params['title'],
                    description = params['description'],
                    price = float(params['price']),
                    selling_price = float(params['selling_price']),
                    category_id=params['category'],
                    subs_category_id = params['subs_category'],
                    product_quantity = params['product_quantity'],
                    insured_amount = float(params['insured_amount']) if params['insured_amount'] else None ,
                    product_weight = float(params['product_weight']) if params['product_weight'] else None,
                    product_height = float(params['product_height']) if params['product_height'] else None,
                    product_depth =  float(params['product_depth']) if params['product_depth'] else None,
                    product_width =  float(params['product_width']) if params['product_width'] else None
                )

            if request.POST.get('in_stock') == 'on':
                product.in_stock = True
            else:
                 product.in_stock = False
            if not request.POST.get('feature'):
                product.feature = request.POST.get('feature')

            if request.FILES.get('image',None):
                upresult = upload(request.FILES['image'])
                product.image = upresult['url']
            product.save()
           
            # ###   Payment Method
            payment_pay = Payment_method(product=product)
            if request.POST.get('payment_method_case_on_delivery', None):
                payment_pay.case_on_delivery = True
            if request.POST.get('payment_method_online_payment', None):
                payment_pay.online_payment = True
            if request.POST.get('payment_method_paypal', None):
                payment_pay.paypal = True
            if request.POST.get('services', None):
                payment_pay.services = request.POST.get('services')
            payment_pay.save()
            
            # # Product color management
            if request.POST.get('total_color',None):
                total_colors = int(request.POST.get('total_color',None))
                response_total_colors = int(request.POST.get('response_total_color',0))
                print("total_colors",response_total_colors)
                print("total_colors",total_colors)
                if total_colors != response_total_colors:
                    total_colors = total_colors - 1
                    while total_colors >= 0:
                        color = Product_color.objects.create(color=params['product_colors-{}-color'.format(total_colors)],
                                                             product = product)
                        for x in range(0, len(request.FILES)):
                            img = request.FILES.get('product_colors-{0}-product_color_images-{1}-product_images'.format(str(total_colors),str(x)), None)
                            if img:
                                uploaedimg = upload(img)
                                Product_Image.objects.create(product_images=uploaedimg['url'],product_colr=color)
                        total_colors = total_colors-1
                else:
                    pass
            pusher_client = pusher.Pusher(app_id='296636',
            							  key='8d36327fa3019f8c74ac',
            							  secret='7c352f5a8fe248126f0e',
            							  cluster='ap2',
            							  ssl=True
            							)
            pusher_client.trigger('juntos_peru', 'click change load', {'message': product.title,'image':product.image.name,'slug':product.slug})
            messages.success(request, 'Product added successfully.')
            return render(request, 'vendor/add-new-product.html', {"categories":category, "add_form":form})
        else:
            return render(request, 'vendor/add-new-product.html', {"categories":category, "add_form":form})
    else:
        category = Category.objects.all()
        return render(request, 'vendor/add-new-product.html',{"categories":category})

class AddProduct(View):
	"""docstring for AddProduct"""
	def get(self,request):
		return render(request, 'vendor/add-new-product.html')
	def post(self,request):
		image_Array = (request.POST.get("muti_image_array")).split()
		print("Image",image_Array)
		params = request.POST
		files = request.FILES
		params['vendor'] = request.user.id
		if 'product_id' in params:
			print("here")
			product = ProductsManagement.objects.get(id=request.POST['product_id'])
			form = NewProductAddForm(params or None,instance=product)
			image_Array = product.image + image_Array if product.image else [] + image_Array
			print(image_Array)
		else:
			form = NewProductAddForm(params or None ,files or None)
		if form.is_valid():
			product = form.save()
			product.expiryDate()
			product.is_active = True
			for i in image_Array:
				print("cfdff",i)
				if i == '' or i == None:
					image_Array.remove(i)
			print(image_Array)
			product.image = image_Array
			product.save()
			if request.POST.get('total_color',None):
				totalColor = int(request.POST.get('total_color',None))
				while totalColor >= 1:
					if "product-colors-{}-color".format(totalColor) in params:
						for x in range(0, len(request.FILES)+1):
							if 'product-colors-{}-product-color-images-{}-product-images'.format(totalColor,x) in request.FILES:
								color = ProductColor.objects.get_or_create(color=params['product-colors-{}-color'.format(totalColor)],product=product)
								print("Color",color)
								img = request.FILES.get('product-colors-{}-product-color-images-{}-product-images'.format(totalColor,x))
								print(img)
								if img:
									uploaedimg = upload(img)
									ProductImage.objects.get_or_create(product_images=uploaedimg['url'],product_color=color[0])
					totalColor = totalColor-1
			messages.success(request, 'Product {} successfully'.format("updated" if 'product_id' in params else "added"))
			return redirect("Vendor:product-list", 1)
		else:
			return render(request, 'vendor/add-new-product.html',{"add_form":form,"image":request.POST.get("muti_image_array").split(',')})


class UpdateProduct(View):
	"""docstring for UpdateProduct"""
	def get(self,request,slug=None):
		user = request.user
		try:
			product = ProductsManagement.objects.get(vendor=user,slug=slug)
			return render(request, 'vendor/update-product.html',{'add_form':product})
		except Exception as e:
			print("Exception--------",e)
			messages.error(request, "Product may not exists or wrong url typed !")
			return redirect("Vendor:vendor-dashboard")

class ProductList(View):
	"""docstring for ProductList"""
	def get(self,request,active=None):
		user  = request.user
		product = ProductsManagement.objects.filter(vendor=user,is_active=active).exclude(expiry_date__lt=datetime.now()).order_by('category','subs_category')
		paginator = Paginator(product, 100)
		page = request.GET.get('page')
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request, 'vendor/product-list.html', {'product_lists':data,'active':True if active=='1' else False})


class ExpiredProductList(View):
	"""docstring for ExpiredProductList"""
	def get(self,request):
		user  = request.user
		product = ProductsManagement.objects.filter(Q(expiry_date__lt=datetime.now())| Q(expiry_date__isnull=True),vendor=user).order_by('category','subs_category')
		paginator = Paginator(product, 100)
		page = request.GET.get('page')
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request, 'vendor/product-list.html', {'product_lists':data,'active':False,"expired":True})
		

class RemoveProduct(View):
	"""docstring for RemoveProduct"""
	def get(self,request,pk=None):
		vendor = request.user
		params = request.POST
		product = ProductsManagement.objects.get(id=pk,vendor=request.user)
		product.is_active = False if product.is_active else True
		active = 0 if product.is_active else 1
		product.save()
		return redirect("Vendor:product-list", active)


def quantityChange(request):
	params = request.POST
	product = ProductsManagement.objects.get(id=params['product'],vendor=request.user)
	product.product_quantity = params['quantity']
	product.save()
	return HttpResponse({"status":200})

class UpdateExpiryDate(View):
	"""docstring for UpdateExpiryDate"""
	def get(self,request,pk=None):
		user = request.user
		try:
			product = ProductsManagement.objects.get(id=pk,vendor=user)
			product.expiryDate()
			return redirect("Vendor:product-list", 0)
		except Exception as e:
			print("Exception",e)
			messages.error(request, "Product may not exists or wrong url typed !")
			return redirect("Vendor:vendor-dashboard")
		

class Notification(View):
	"""docstring for AddNotification"""
	def get(self,request,read=None):
		user = request.user
		if user.is_vendor:
			notifications = Notifications.objects.filter(vendor=user,is_read=read).order_by('-created_at')
			return render(request, 'vendor/notifications.html', {'notifications':notifications})
		else:
			messages.error(request, "You are not authorize to access this page.")
			return redirect("Vendor:bevendor")

@login_required(login_url="vendor:bevendor")
def payment_transaction_details(request):
    payments = CustomerTransactionDetails.objects.filter(reciever_email=request.user.email)
    return render(request, 'vendor/payment.html', {"payments":payments, "notification_unread_count":unread_count(request.user)})

class PaymentTransactionDetails(View):
	"""docstring for PaymentTransactionDetails"""
	def get(self,request):
		return render(request, 'vendor/payment.html')
		


class DhlPage(View):
	"""docstring for DhlPage"""
	def get(self,request):
		return render(request, 'vendor/dhl_credential.html')



class UploadedProducts(View):
	"""docstring for UploadedProducts"""
	def get(self,request):
		user = request.user
		previous_products = Products_Management.objects.filter(vendor=user, expire_products=0)
		return render(request,'vendor/uploaded_products.html',{"previous_products":previous_products})


	
class SellingChart(View):
	"""docstring for SellingChart"""
	def get(self,request):
		return redirect('Vendor:vendor-dashboard')
	

# def dhl_credentials(request):
#     # print("reeeeeeeeeeeeeeeeeeeeeeeee",request)
#     if request.method == 'POST':
#         params = request.POST
#         # params['vendor_id'] = request.user.id
#         form = DHL_Form(params  or None)
#         if form.is_valid():
#             result = form.save(commit=False)
#             result.vendor = request.user
#             result.save()
#             messages.success(request, "Dhl Credentials added successfully")
#             return redirect('vendor:dhl_credential')
#         else:
#             print("Errors",form.errors)
#             messages.error(request, "Dhl Credentials not added")
#             return redirect('vendor:dhl_credential')
#     return render(request, 'vendor/dhl_credential.html')

class DhlCredentials(View):
	"""docstring for DhlCredentials"""
	def get(self,request):
		return render(request, 'vendor/dhl_credential.html')
	

class SubCategoryList(View):
	"""docstring for SubCategoryList"""
	def post(self,request):
		params =request.POST
		category = params['category_id']
		data = SubCategory.objects.filter(category_id=category)
		dictionaries = [ obj.as_dict() for obj in data ]
		datas = json.dumps({"data": dictionaries})
		return HttpResponse(datas, content_type='application/json')




class GetSubCategoryTag(View):
	"""docstring for GetSubCategoryTag"""
	def post(self,request):
		params = request.POST
		subcategory = params['subcategory_id']
		data = SubCategory.objects.get(id=subcategory)
		datas = json.dumps({"data": data.sub_category_tag})
		return HttpResponse(datas, content_type='application/json')


class GetProductSize(View):
	"""docstring for GetProductSize"""
	def post(self,request):
		params = request.POST
		parent = params['value']
		data = AvailableSize.objects.filter(parent__p_type=parent)
		dictionaries = [ obj.size for obj in data ]
		datas = json.dumps({"data": dictionaries})
		return HttpResponse(datas, content_type='application/json')

class ProfileView(View):
	"""docstring for ProfileView"""
	# @login_required(login_url="vendor:bevendor")
	def get(self,request):
		user = request.user
		if user.is_vendor:
			return render(request, "vendor/profile.html") 
		else:
			messages.error(request, "You are not authorize to access this page.")
			return redirect("Vendor:bevendor")

class UpdateProfile(View):
	"""docstring for UpdateProfile"""
	# @login_required(login_url="Vendor:bevendor")
	def post(self,request):
		user = request.user
		if user.is_vendor:
			params = request.POST
			files = request.FILES
			form = ProfileVendorForm(request.POST or None)
			if form.is_valid():
				user.first_name = params['first_name']
				user.account.address1 = params['address1']
				user.account.address2 = params['address2']
				user.city = params['city']
				user.pincode = params['pincode']
				user.account.legal_name = params['legal_name']
				user.state = params['state']
				if "image" in files:
					for img in files.getlist('image'):
						upresult = upload_resource(img)
						user.avatar = upresult
				user.save()
				bank_detail = user.account
				bank_detail.business_name = params['business_name']
				bank_detail.account_number = params['account_number']
				bank_detail.routing_number = params['routing_number']
				bank_detail.bank_name = params['bank_name']
				bank_detail.save()
				messages.success( request, 'Profile Updated')
				return redirect("Vendor:vendor-profile-view")
			else:
				print("Error",form.errors)
				return render(request, 'vendor/profile.html',{"vendor_profile_form":form,"user":user})
		else:
			messages.error(request, "You are not authorize to access this page.")
			return redirect("Vendor:bevendor")

@login_required(login_url="vendor:bevendor")
def order_details(request, order_id):
    user = request.user
    order_detail['mode_of_transport'] = shipping_address.mode_of_transport
    order_detail['order_payment_type'] = order_data.order_id.order_payment_type

class OrderDetails(View):
	"""docstring for OrderDetails"""
	def get(self,request,order_id=None):
		orders = OrderItems.objects.get(id=order_id)
		try:
			invoice_exist = CustomerOrderInvoice.objects.get(item_order_id_id=order_id)
			invoice = False
		except Exception as e:
			print("Exception as e",e)
			invoice = True
		address = orders.order.customer.shiping_address.all().latest('created_at')
		return render(request, 'vendor/order-details.html',{"orders":orders,"address":address,"invoice":invoice})


class RemoveNotification(View):
	"""docstring for RemoveNotification"""
	def get(self,request,pk=None):
		notify = Notifications.objects.get(vendor=request.user, id=pk)
		notify.is_read= True
		notify.save()
		return redirect("Vendor:notifications", 0)
			
class DeleteColors(View):
	"""docstring for DeleteColors"""
	def post(self,request):
		params = request.POST
		try:
			ProductColor.objects.get(id=params['id']).delete()
			return HttpResponse({"status":200,"message": "Successfully Deleted"}, content_type='application/json')
		except Exception as e:
			print("Exception is ------",e)
			return HttpResponse({"status":500,"message": "Not Deleted Successfully"}, content_type='application/json')



@login_required(login_url="/")
def view_order(request):
    orders = CustomerOrder_items.objects.filter(order_id__customer=request.user, order_cancel_request=False)
    if orders:
        total_price=[]
        for order in orders:
            price = order.price
            grand_total = (price*23)/100
            total_price.append(grand_total + price)
        paginator = Paginator(orders, 8)
        index=1
        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        return render(request, 'orders.html' , {'orders':orders,"total_price":total_price})
    return render(request, 'orders.html' , {'orders':orders})


class VendorViewOrder(View):
	"""docstring for ViewOrder"""
	def get(self,request):
		print("GET")
		orders = OrderItems.objects.filter(order__customer=request.user,order_cancel_request=False)
		return render(request, 'vendor/view-order.html',{'orders':orders})
	def post(self,request):
		print("POST")
		return render(request, 'vendor/view-order.html')		

class InvoiceOrder(View):
	"""docstring for InvoiceOrder"""
	def get(self,request):
		print("GET----------------------")
		return redirect("vendor:order-details",request.POST['order_id'] )

	def post(self,request):
		print("POST----------------------")
		if request.user.is_vendor:
			try:
				invoice_exist = CustomerOrderInvoice.objects.get(item_order_id_id=int(request.POST['order_id']))
				messages.info(request, "Invoice for the same order already exits.")
				return redirect("Vendor:order-details",request.POST['order_id'] )
			except Exception as e:
				print("Exception",e)
				form = CreateInvoiceForm(request.POST or None)
				if form.is_valid():
					order_data = OrderItems.objects.get(id=request.POST['order_id'])
					invoice = CustomerOrderInvoice(item_order_id=order_data)
					invoice.shippment_date = datetime.strptime(request.POST['shippment_date'],'%m/%d/%Y').strftime('%Y-%m-%d')
					invoice.pickup_date = datetime.strptime(request.POST['pickup_date'],'%m/%d/%Y').strftime('%Y-%m-%d')
					invoice.ready_by_time = request.POST['ready_by_time']
					invoice.close_time = request.POST['close_time']
					invoice.shipping_charge = order_data.shipping_charge
					invoice.billing_info = order_data.order.shipping_address.id
					invoice.shipping_info = order_data.order.shipping_address.id
					invoice.payment_method = order_data.order.order_payment_type
					invoice.save()
					vendor_dhl = request.user
					# dhl_service(order_data, vendor_dhl, invoice)
					messages.info(request, "Invoice # {1} for order # {0} has generated.".format(order_data.order.order_number, invoice.invoice_number))
					return render(request, "vendor/order-invoice.html",{"order_data":order_data,"invoice":invoice,'current_date':datetime.now()})
				else:
					orders = OrderItems.objects.get(id=request.POST['order_id'])
					address = orders.order.customer.shiping_address.all().latest('created_at')
					return render(request, 'vendor/order-details.html',{"orders":orders,"address":address,"form":form})
		else:
			return redirect('Juntos:home')


class DeleteProductImage(View):
	"""docstring for DeleteProductImage"""
	def post(self,request):
		params = request.POST
		print(params)
		product = ProductsManagement.objects.get(id=params['product'])
		product.image.remove(params['img'])
		product.save()
		return JsonResponse({"status":200,"image":product.image})

class UploadImage(View):
	"""docstring for UploadImage"""

	def post(self,request):
		params = request.POST
		upresult = upload(params['image'])
		return JsonResponse({"status":200,"image":upresult['url']})
	
		
																		
																																														