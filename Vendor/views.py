from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cloudinary.uploader import upload
import os
# from django.http import QueryDicta
import base64
import json
from Juntos.models import *
from .forms import *

def unread_count(vendor):
    count = Notifications.objects.filter(vendor=vendor, is_read=False).count()
    return  count
# def vendor_signup(request):
#     form = VendorRegistrationForm1()
#     if request.method == 'POST':
#         user = request.user
#         vendor = MyUser.objects.get(id=user.id)
#         # print(user)
#         params = request.POST
#         # print("------requst data--------",request.POST)
#         if params['step'] == "validate":
#             form = VendorRegistrationForm1(params or None, instance=vendor)
#             if form.is_valid():
#                 if request.FILES.get('avatar', None):
#                     upresult = upload(request.FILES['avatar'])   ####  upload images
#                     # request.session['avatar'] = upresult['url']
#                     vendor.avatar = upresult['url']
#                 vendor.is_vendor = True
#                 vendor.is_customer = True
#                 vendor.save()
#                 form = VendorRegistrationForm2()
#                 # messages.success(request, 'Mobile verification success.')
#                 return render(request, 'vendor/registration_form2.html', {'vendor': form})
#             else:
#                 return render(request, 'vendor/registration_form1.html', {'vendor': form})

#         elif params['step'] == 'step2':
#             try:
#                 form = VendorRegistrationForm2(params)
#                 if form.is_valid():
#                     request.session['business_name'] = params['business_name']
#                     request.session['legal_name']    = params['legal_name']
#                     request.session['address1']      = params['address1']
#                     request.session['address2']      = params['address2']
#                     messages.success(request, 'Seller business information saved.')
#                     form = VendorRegistrationForm3()
#                     return render(request, 'vendor/registration_form3.html', {'vendor': form})
#                 else:
#                     return render(request, 'vendor/registration_form2.html', {'vendor': form})
#             except Exception  as a:
#                 print("error",a)
#                 return render(request, 'vendor/registration_form3.html', {'vendor': form})

#         elif params['step'] == 'step3':
#             form = VendorRegistrationForm3(params)
#             # print(form)
#             if form.is_valid():
#                 bank = Vendor_Account_Details.objects.create(vendor=vendor,
#                                               bank_name=params['bank_name'],
#                                               routing_number=params['routing_number'],
#                                               account_number=params['account_number'],
#                                               agree_terms_condition=True,
#                                               address1=request.session['address1'],
#                                               address2=request.session['address2'],
#                                               legal_name=request.session['legal_name'],
#                                               business_name=request.session['business_name'],
#                                               )
#                 messages.info(request, 'Signing up success.')
#                 return redirect('vendor:vendor_dashboard')
#             else:
#                 print("step3")
#                 return render(request, 'vendor/registration_form3.html', {'vendor': form})
#         else:
#             print("step1")
#             return render(request, 'vendor/registration_form1.html', {'vendor': form})
#     else:
#         return render(request, 'vendor/registration_form1.html')



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
				# print(request.FILES)
				# upresult = upload(request.FILES['avatar'])
				# user.avatar = upresult
				# user.is_vendor = True
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



# @login_required(login_url="vendor:bevendor")
# @register.filter(is_safe=True, name='lookup')
# def vendor_dashboard(request):
#     vendor = request.user
#     if (vendor.is_vendor and vendor.is_active):
#         try:
#             vendor.account
#             account = False
#         except:
#             account = True
#         total_customer = MyUser.objects.filter(is_customer=True, is_active=True).count()
#         order_data = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__day=datetime.today().day).order_by('-created_at')
#         total_sell = order_data.aggregate(Sum('product__selling_price'))['product__selling_price__sum']
#         total_sell = total_sell if total_sell else  0.0
#         total_order = CustomerOrder_items.objects.filter(product__vendor=request.user).count()
#         total_product = Products_Management.objects.filter(vendor=vendor)
#         order_hash = []
#         record_chart_array = [['Year', 'Sales', 'Expenses', 'Profit']]
#         for product in total_product:
#             if product.order.exists():
#                 order_item_list = product.order.filter(created_at__day=datetime.today().day)
#                 for order in order_item_list:
#                     if not any( orderl.get('id') == order.product.id for orderl in order_hash):
#                         sales = order_item_list.filter(product_id=order.product.id).aggregate(Sum('price'))['price__sum']
#                         total_original_price = order_item_list.filter(product_id=order.product.id).count() * order.product.price
#                         print(total_original_price)
#                         total_expenses_price = order_item_list.filter(product_id=order.product.id).count() * order.product.selling_price
#                         order_hash.append({"id":order.product.id,"title":order.product.title, "sales":sales,"profit":order.price-total_original_price,"expenses":order.price-total_expenses_price})
#                     else:
#                         pass
#         if order_hash:
#             for record in order_hash:
#                 record_chart_array.append([str(record['title']),record['sales'],record['expenses'],record['profit']])
#         else:
#             for product1 in total_product:
#                 record_chart_array.append([str(product1.title), 0.0,0.0,0.0])

#         # return render(request, 'vendor/dashboard.html',{"total_customer":total_customer,"notification_unread_count":unread_count(vendor) ,"ajax":None, "sell_hash": record_chart_array,"total_sell":total_sell, "total_order":total_order, "account": account})
#         return render(request, 'vendor/dashboard.html',{"total_customer":total_customer,"notification_unread_count":unread_count(vendor) ,"ajax":None, "sell_hash": record_chart_array,"total_sell":total_sell, "total_order":total_order, "account": account})
#     elif(vendor.is_vendor):
#         messages.info(request, "You have received confirmation email, Please confirm your email.")
#         return redirect("vendor:bevendor")
#     else:
#         messages.error(request, "You are not authorize to access this page.")
#         return redirect("Vendor:bevendor")
		
class VendorDashboard(View):
	"""docstring for VendorDashboard"""
	def get(self,request):
		return render(request, 'vendor/dashboard.html')
	

class BVendor(View):
	"""docstring for BVendor"""
	def get(self,request):
		return redirect('Juntos:home')




# def logout_view(request):
#     logout(request)
#     return redirect("vendor:bevendor")

class LogoutView(View):
	"""docstring for LogoutView"""
	def get(self,request):
		logout(request)
		return redirect("Vendor:bevendor")


# def change_password(request):
#     form = ChangePasswordForm(user=request.user)
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST, user=request.user)
#         if form.is_valid():
#             user = request.user
#             user.set_password(request.POST.get('new_password', user.password))
#             user.save()
#             update_session_auth_hash(request, form.user)
#             # user = authenticate(username=user.email, password=user.password)
#             # login(request, user)
#             messages.success(request, "Password changed successfully.")
#             return redirect("vendor:vendor_dashboard")
#         else:
#             return render(request,'vendor/change_password.html',{"forms":form})
#     else:
#         return render(request,'vendor/change_password.html',{"forms":form})


class ChangePassword(View):
	"""docstring for ChangePassword"""
	def post(self,request):
		form = ChangePasswordForm(request.POST, user=request.user)
		if form.is_valid():
			user = request.user
			user.set_password(request.POST.get('new_password', user.password))
			user.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, "Password changed successfully.")
			return redirect("Vendor:vendor_dashboard")
		else:
			return render(request,'vendor/change_password.html',{"forms":form})





class ProductList(View):
	"""docstring for ProductList"""
	def get(self,request):
		user  = request.user
		product = ProductsManagement.objects.filter(vendor=user).order_by('-created_at')
		paginator = Paginator(product, 5)
		page = request.GET.get('page')
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request, 'vendor/product-list.html', {'product_lists':data,"notification_unread_count":unread_count(request.user)})


# @login_required(login_url="vendor:bevendor")
# def order_history(request):
#     order_data = CustomerOrder_items.objects.filter(product__vendor=request.user).order_by('-created_at')
#     total_order = order_data.count()
#     paginator = Paginator(order_data, 10)
#     page = request.GET.get('page')
#     try:
#         orders = paginator.page(page)
#     except PageNotAnInteger:
#         orders = paginator.page(1)
#     except EmptyPage:
#         orders = paginator.page(paginator.num_pages)
#     return render(request, 'vendor/order-history.html',{"notification_unread_count":unread_count(request.user),'order_data':orders, 'total_order':total_order})	
class OrderHistory(View):
	"""docstring for OrderHistory"""
	def get(self,request):
		return render(request, 'vendor/order-history.html')

def add_product(request):
    try:
        product = Products_Management.objects.get(id=request.POST['product_id'])
    except Exception as e:
        print('Error in Product Management',e)
        product = False
    # print(product)
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
            return render(request, 'vendor/add-new-product.html', {"categories":category, "add_form":form, "notification_unread_count":unread_count(request.user)})
        else:
            return render(request, 'vendor/add-new-product.html', {"categories":category, "add_form":form, "notification_unread_count":unread_count(request.user)})
    else:
        category = Category.objects.all()
        return render(request, 'vendor/add-new-product.html',{"categories":category, "notification_unread_count":unread_count(request.user)})

class AddProduct(View):
	"""docstring for AddProduct"""
	def get(self,request):
		return render(request, 'vendor/add-new-product.html')
	def post(self,request):
		image_Array = []
		queryset = ProductsManagement.objects.all()
		params = request.POST
		files = request.FILES
		params['vendor'] = request.user.id
		form = NewProductAddForm(params or None)
		if form.is_valid():
			product = form.save()
			if "image" in files:
				for img in files.getlist('image'):
					upresult = upload(img)
					image_Array.append(upresult['url'])
				product.image = image_Array
				product.save()
			messages.success(request, 'Product added successfully')
			return redirect("Vendor:product-list")
		else:
			print("Errors",form.errors)
			for img in files.getlist('image'):
				h=img.path				
				print(h)
				image_Array.append(h)
			return render(request, 'vendor/add-new-product.html',{"add_form":form,"notification_unread_count":unread_count(request.user),"image":image_Array})

@login_required(login_url="vendor:bevendor")
def add_notification(request):
    if request.user.is_vendor:
        notifications = Notifications.objects.filter(vendor=request.user).order_by('-created_at')
        data = []
        for noti in notifications:
            data.append({'id': noti.id, 'content': noti.content, 'created_at': str(noti.created_at.date()), "time": str(natural_time(noti.created_at))})
        def extract_date(entity):
            return entity['created_at']
        list_of_lists = [list(g) for t, g in groupby(data, key=extract_date)]
        booking_arr = []
        for i in range(0, len(list_of_lists)):
            booking_hash = {}
            booking_hash["date"] = str(list_of_lists[i][0]['created_at'])
            booking_hash["notify"] = list_of_lists[i]
            booking_arr.append(booking_hash)
        notifications.filter(is_read=False).update(is_read=True)
        if booking_arr:
            notify = booking_arr[0]['notify'][:3]
        else:
            notify = []
        return render(request, 'vendor/notifications.html', {'notifications':booking_arr,"notify":notify, "notification_unread_count":unread_count(request.user)})
    else:
        messages.error(request, "You are not authorize to access this page.")
        return redirect("vendor:bevendor")
	
class AddNotification(View):
	"""docstring for AddNotification"""
	def get(self,request):
		user = request.user
		if user.is_vendor:
			notifications = Notifications.objects.filter(vendor=user).order_by('-created_at')
			# return render(request, 'vendor/notifications.html', {'notifications':booking_arr,"notify":notify, "notification_unread_count":unread_count(request.user)})
			return render(request, 'vendor/notifications.html', {'notifications':notifications, "notification_unread_count":unread_count(request.user)})
		else:
			messages.error(request, "You are not authorize to access this page.")
			return redirect("Vendor:bevendor")

# @login_required(login_url="vendor:bevendor")
# def payment_transaction_details(request):
#     payments = CustomerTransactionDetails.objects.filter(reciever_email=request.user.email)
#     return render(request, 'vendor/payment.html', {"payments":payments, "notification_unread_count":unread_count(request.user)})

class PaymentTransactionDetails(View):
	"""docstring for PaymentTransactionDetails"""
	def get(self,request):
		return render(request, 'vendor/payment.html')
		


class DhlPage(View):
	"""docstring for DhlPage"""
	def get(self,request):
		return render(request, 'vendor/dhl_credential.html')


# def uploaded_products(request):
#     try:
#         user = request.user
#         # print("userrrrrrrrrr",user)
#         previous_products = Products_Management.objects.filter(vendor=user, expire_products=0)
#         return render(request, 'vendor/uploaded_products.html',{"previous_products":previous_products})
#     except Exception as e:
#         print(e,)
#         return redirect('Peru:home')
	
class UploadedProducts(View):
	"""docstring for UploadedProducts"""
	def get(self,request):
		user = request.user
		previous_products = Products_Management.objects.filter(vendor=user, expire_products=0)
		return render(request,'vendor/uploaded_products.html',{"previous_products":previous_products})



# @login_required(login_url="vendor:bevendor")
# def selling_chart(request, query):
#     vendor = request.user
#     if query =='day':
#         # print("-------------query------",query)
#         total_customer = MyUser.objects.filter(is_customer=True, is_active=True, created_at__day=datetime.today().day).count()
#         order_data     = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__day=datetime.today().day).order_by('-created_at')
#         total_sell     = order_data.aggregate(Sum('product__selling_price'))['product__selling_price__sum']
#         total_sell     = total_sell if total_sell else  0.0
#         total_order    = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__day=datetime.today().day).count()
#         total_product  = Products_Management.objects.filter(vendor=vendor)
#         order_hash = []
#         record_chart_array = [['Year', 'Sales', 'Expenses', 'Profit']]
#         for product in total_product:
#             if product.order.exists():
#                 order_item_list = product.order.filter(created_at__day=datetime.today().day)
#                 for order in order_item_list:
#                     if not any( orderl.get('id') == order.product.id for orderl in order_hash):
#                         sales = order_item_list.filter(product_id=order.product.id).aggregate(Sum('price'))['price__sum']
#                         total_original_price = order_item_list.filter(product_id=order.product.id).count() * order.product.price
#                         total_expenses_price = order_item_list.filter(product_id=order.product.id).count() * order.product.selling_price
#                         order_hash.append({"id":order.product.id,"title":order.product.title, "sales":sales,"profit":order.price-total_original_price,"expenses":order.price-total_expenses_price})
#                     else:
#                         pass
#         if order_hash:
#             for record in order_hash:
#                 record_chart_array.append([str(record['title']),record['sales'],record['expenses'],record['profit']])
#         else:
#             for product1 in total_product:
#                 record_chart_array.append([str(product1.title), 0.0,0.0,0.0])
#         # print(record_chart_array)
#         return render(request,'vendor/partial-dashboard.html' ,{"sell_hash":record_chart_array,"notification_unread_count":unread_count(request.user) ,"ajax":"Day", "total_customer":total_customer,"total_sell":total_sell, "total_order":total_order})
#     if query=='month':
#         total_customer = MyUser.objects.filter(is_customer=True, is_active=True, created_at__month=datetime.today().month).count()
#         order_data     = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__month=datetime.today().month).order_by('-created_at')
#         total_sell     = order_data.aggregate(Sum('product__selling_price'))['product__selling_price__sum']
#         total_sell     = total_sell if total_sell else  0.0
#         total_order    = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__month=datetime.today().month).count()
#         total_product  = Products_Management.objects.filter(vendor=vendor)
#         order_hash = []
#         record_chart_array = [['Year', 'Sales', 'Expenses', 'Profit']]
#         for product in total_product:
#             if product.order.exists():
#                 order_item_list = product.order.filter(created_at__month=datetime.today().month)
#                 for order in order_item_list:
#                     if not any( orderl.get('id') == order.product.id for orderl in order_hash):
#                         sales = order_item_list.filter(product_id=order.product.id).aggregate(Sum('price'))['price__sum']
#                         total_original_price = order_item_list.filter(product_id=order.product.id).count() * order.product.price
#                         total_expenses_price = order_item_list.filter(product_id=order.product.id).count() * order.product.selling_price
#                         order_hash.append({"id":order.product.id,"title":order.product.title, "sales":sales,"profit":order.price-total_original_price,"expenses":order.price-total_expenses_price})
#                     else:
#                         pass
#         if order_hash:
#             for record in order_hash:
#                 record_chart_array.append([str(record['title']),record['sales'],record['expenses'],record['profit']])
#         else:
#             for product1 in total_product:
#                 record_chart_array.append([str(product1.title), 0.0,0.0,0.0])
#         return render(request,'vendor/partial-dashboard.html' ,{"notification_unread_count":unread_count(request.user),"sell_hash": record_chart_array,"ajax":'Month',"total_customer":total_customer,"total_sell":total_sell, "total_order":total_order})
#     if query=='year':
#         total_customer = MyUser.objects.filter(is_customer=True, is_active=True, created_at__year=datetime.today().year).count()
#         order_data     = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__year=datetime.today().year).order_by('-created_at')
#         total_sell     = order_data.aggregate(Sum('product__selling_price'))['product__selling_price__sum']
#         total_sell     = total_sell if total_sell else  0.0
#         total_order    = CustomerOrder_items.objects.filter(product__vendor=request.user, created_at__year=datetime.today().year).count()
#         total_product  = Products_Management.objects.filter(vendor=vendor)
#         order_hash = []
#         record_chart_array = [['Year', 'Sales', 'Expenses', 'Profit']]
#         for product in total_product:
#             if product.order.exists():
#                 order_item_list = product.order.filter(created_at__year=datetime.today().year)
#                 for order in order_item_list:
#                     if not any( orderl.get('id') == order.product.id for orderl in order_hash):
#                         sales = order_item_list.filter(product_id=order.product.id).aggregate(Sum('price'))['price__sum']
#                         total_original_price = order_item_list.filter(product_id=order.product.id).count() * order.product.price
#                         total_expenses_price = order_item_list.filter(product_id=order.product.id).count() * order.product.selling_price
#                         order_hash.append({"id":order.product.id,"title":order.product.title, "sales":sales,"profit":order.price-total_original_price,"expenses":order.price-total_expenses_price})
#                     else:
#                         pass
#         if order_hash:
#             for record in order_hash:
#                 record_chart_array.append([str(record['title']),record['sales'],record['expenses'],record['profit']])
#         else:
#             for product1 in total_product:
#                 record_chart_array.append([str(product1.title), 0.0,0.0,0.0])
#         return render(request,'vendor/partial-dashboard.html' ,{"notification_unread_count":unread_count(request.user),"sell_hash": record_chart_array,"ajax":'Year' ,"total_customer":total_customer,"total_sell":total_sell, "total_order":total_order})
#     else:
#         messages.info(request, "Entered query may be wrong !")
#         return redirect('vendor:vendor_dashboard')

	
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
	
# @login_required
# def sub_category_list(request):
#     category = request.POST['category_id']
#     data = Sub_Category.objects.filter(category_id=category)
#     dictionaries = [ obj.as_dict() for obj in data ]
#     datas = json.dumps({"data": dictionaries})
#     # print("----",datas)
#     return HttpResponse(datas, content_type='application/json')

class SubCategoryList(View):
	"""docstring for SubCategoryList"""
	def post(self,request):
		params =request.POST
		category = params['category_id']
		data = SubCategory.objects.filter(category_id=category)
		dictionaries = [ obj.as_dict() for obj in data ]
		datas = json.dumps({"data": dictionaries})
		return HttpResponse(datas, content_type='application/json')


# def GetSubCategoryTag(request):
#     if request.POST.get('subcategory_id', None):
#         subcategory = request.POST['subcategory_id']
#         data = Sub_Category.objects.get(id=subcategory)
#         # dictionaries = [ obj.as_dict() for obj in data ]
#         datas = json.dumps({"data": data.sub_category_tag})
#         return HttpResponse(datas, content_type='application/json')

class GetSubCategoryTag(View):
	"""docstring for GetSubCategoryTag"""
	def post(self,request):
		params = request.POST
		subcategory = params['subcategory_id']
		data = SubCategory.objects.get(id=subcategory)
		datas = json.dumps({"data": data.sub_category_tag})
		return HttpResponse(datas, content_type='application/json')

class ProfileView(View):
	"""docstring for ProfileView"""
	# @login_required(login_url="vendor:bevendor")
	def get(self,request):
		user = request.user
		if user.is_vendor:
			return render(request, "vendor/profile.html",{"user":user, "notification_unread_count":unread_count(request.user)}) 
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
			form = ProfileVendorForm(request.POST or None)
			if form.is_valid():
				user.first_name = params['first_name']
				user.account.address1 = params['address1']
				user.account.address2 = params['address2']
				user.city = params['city']
				user.pincode = params['pincode']
				user.account.legal_name = params['legal_name']
				user.state = params['state']
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
				return render(request, 'vendor/profile.html',{"vendor_profile_form":form,"user":user,"notification_unread_count":unread_count(request.user)})
		else:
			messages.error(request, "You are not authorize to access this page.")
			return redirect("Vendor:bevendor")




# @login_required(login_url='vendor:bevendor')
# def update_product(request,slug):
#     vendor = request.user
#     try:
#         categories = Category.objects.all()
#         sub_cate   = Sub_Category.objects.all()
#         product    = Products_Management.objects.get(vendor=vendor, slug=slug)
#         total_image = Product_Image.objects.filter(product_colr__product__slug=slug).count()
#         total_color = product.product_colors.count()
#         return render(request, 'vendor/update-product.html',{'edit_form':product,"total_image":total_image,"total_color":total_color,"categories":categories,"sub_cate":sub_cate,"notification_unread_count":unread_count(request.user)})
#     except:
#         messages.error(request, "Product may not exists or wrong url typed !")
#         return redirect("vendor:vendor_dashboard")


class UpdateProduct(View):
	"""docstring for UpdateProduct"""
	def get(self,request,slug=None):
		queryset = ProductsManagement.objects.all()
		user = request.user
		try:
			product = ProductsManagement.objects.get(vendor=user,slug=slug)
			return render(request, 'vendor/update-product.html',{'edit_form':product})
		except Exception as e:
			print("Exception",e)
			messages.error(request, "Product may not exists or wrong url typed !")
			return redirect("Vendor:vendor-dashboard")

# @login_required(login_url="vendor:bevendor")
# def remove_product(request):
    # vendor = request.user
    # params = request.POST
    # prodct = Products_Management.objects.filter(id=params['product'],vendor=request.user)
    # prodct.delete()
    # products = Products_Management.objects.filter(vendor=vendor).order_by('-created_at')
    # total = products.count()
    # return HttpResponse(json.dumps({"message":"Item removed successfully.", "code":200,'total_product':total}), content_type='application/json')

class RemoveProduct(View):
	"""docstring for RemoveProduct"""
	def post(self,request):
		vendor = request.user
		params = request.POST
		prodct = ProductsManagement.objects.filter(id=params['product'],vendor=request.user)
		prodct.delete()
		products = ProductsManagement.objects.filter(vendor=vendor).order_by('-created_at')
		total = products.count()
		return HttpResponse(json.dumps({"message":"Item removed successfully.", "code":200,'total_product':total}), content_type='application/json')

	
# @login_required(login_url="vendor:bevendor")
# def order_details(request, order_id):
#     user = request.user
#     order_data   = CustomerOrder_items.objects.get(id=order_id)
#     order_detail = {}
#     order_detail['order_id']     = order_id
#     order_detail['order_number'] = order_data.order_id.order_number
#     order_detail['order_date']   = order_data.created_at
#     order_detail['total_price']  = order_data.price
#     order_detail['status']       = str(order_data.delivery_status)
#     order_detail['delivery_date'] = order_data.created_at + timedelta(days=5)
#     order_detail['pickup_time'] = order_data.created_at + timedelta(days=2)
#     order_detail['product_name']  = order_data.product.title
#     order_detail['quantity'] = order_data.quantity
#     order_detail['insured_amount'] = order_data.product.insured_amount
#     order_detail['product_weight'] = order_data.product.product_weight 
#     order_detail['product_height'] = order_data.product.product_height
#     order_detail['product_depth'] = order_data.product.product_depth
#     order_detail['product_width'] = order_data.product.product_width


#     # print("colorrr",order_data.product_color)

#     if  order_data.product_color:
#         try:
#             color = Product_color.objects.get(id = order_data.product_color).color
#         except Exception as e:
#             print("error",e)
#             color = []
#         order_detail['color'] = color
#     if  order_data.product_size:
#         while True:
#             if order_data.product_size == 0:
#                 order_detail['size'] = "Extra Small"
#                 break
#             if order_data.product_size == 1:
#                 order_detail['size'] = "Small"
#                 break
#             if order_data.product_size == 2:
#                 order_detail['size'] = "Medium"
#                 break
#             if order_data.product_size == 3:
#                 order_detail['size'] = "Large"
#                 break
#             if order_data.product_size == 4:
#                 order_detail['size'] = "Extra Large"
#                 break
#     order_detail['customer'] = order_data.order_id.customer.email
#     order_detail['mobile'] = order_data.order_id.customer.mobile
#     shipping_address = order_data.order_id.customer.shiping_address.filter(selected=True)
#     shipping_address = shipping_address.last()
#     order_detail['address'] = shipping_address.s_address
#     order_detail['city'] = shipping_address.s_city
#     order_detail['state'] = shipping_address.s_state
#     order_detail['postcode'] = shipping_address.s_zip
#     order_detail['country'] = shipping_address.s_country
#     order_detail['country_abbriviation'] = shipping_address.s_country_abbriviation
#     order_detail['mode_of_transport'] = shipping_address.mode_of_transport

#     order_detail['order_payment_type'] = order_data.order_id.order_payment_type
#     order_detail["notification_unread_count"] = unread_count(request.user)
#     return render(request, 'vendor/order-details.html', order_detail)

class OrderDetails(View):
	"""docstring for OrderDetails"""
	def get(self,request):
		return render(request, 'vendor/order-details.html', order_detail)

# @login_required(login_url="vendor:bevendor")
# def remove_notification(request, pk):
#     messages.success(request, "Notification removed .")
#     Notifications.objects.filter(vendor=request.user, id=pk).delete()
#     return redirect("vendor:notifications")

class RemoveNotification(View):
	"""docstring for RemoveNotification"""
	def get(self,request):
		return redirect("Vendor:notifications")

	
		
# def delete_colors(request):
#     try:
#         p_c = Product_color.objects.get(id=request.POST['id'])
#         p_c.delete()
#         datas = json.dumps({"status":200,"message": "Successfully Deleted"})
#         return HttpResponse(datas, content_type='application/json')
#     except Exception as e:
#         print('Error',e)
#         datas = json.dumps({"status":500,"message": "Not Deleted Successfully"})
#         return HttpResponse(datas, content_type='application/json')
			
class DeleteColors(View):
	"""docstring for DeleteColors"""
	def get(self,request):
		params = request.POST
		try:
			Product_color.objects.get(id=params['id']).delete()
			return HttpResponse({"status":200,"message": "Successfully Deleted"}, content_type='application/json')
		except:
			return HttpResponse({"status":500,"message": "Not Deleted Successfully"}, content_type='application/json')


# @login_required(login_url="/")
# def view_order(request):
#     # print(request.user.id)
#     orders = CustomerOrder_items.objects.filter(order_id__customer=request.user, order_cancel_request=False)
#     if orders:
#         total_price=[]
#         for order in orders:
#             price = order.price
#             grand_total = (price*23)/100
#             total_price.append(grand_total + price)
#             # print("view_order",total_price)
#         paginator = Paginator(orders, 8)
#         index=1
#         page = request.GET.get('page')
#         try:
#             orders = paginator.page(page)
#         except PageNotAnInteger:
#             orders = paginator.page(1)
#         except EmptyPage:
#             orders = paginator.page(paginator.num_pages)
#         return render(request, 'orders.html' , {'orders':orders,"total_price":total_price})
#     return render(request, 'orders.html' , {'orders':orders})

class ViewOrder(View):
	"""docstring for ViewOrder"""
	def get(self,request):
		return render(request, 'vendor/view-order.html')


			
				
				
																																														