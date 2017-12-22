# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django import template
from django.db.models import Q
from django.db.models import Sum, Avg, Count
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth import (REDIRECT_FIELD_NAME, get_user_model, login as auth_login, logout as auth_logout, update_session_auth_hash, )
from django.contrib.auth.decorators import login_required
from django.views import View
from random import randint
from datetime import datetime, timedelta
import ast
import json
from .twillio import send_sms
from .models import *
from .forms import *
from .decorator import *
from .paypal import *
from Static_Model.models import *

# Create your views here.

def handler404(request):
	print("Juntos 404")
	template = 'index.html'
	return render(request, template)

def csrf_failure(request, reason=""):
	return render_to_response('index.html',{'csrf_error': 'CSRF token has expired or not valid!'})

def bad_request(request):
	response = render_to_response( '400.html', context_instance=RequestContext(request) )
	response.status_code = 400
	return response

def home(request):
	current_date = datetime.now()
	product = ProductsManagement.objects.all().exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False) | Q(recommended=True)).order_by('-created_at')
	paginator = Paginator(product, 15)
	page = request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	offers = Offer.objects.filter(offer_end_date_time__gte=current_date.date())
	hotItems = OrderItems.objects.filter(product__expiry_date__gt=current_date.date()).distinct('product')
	advertiseProducts = Advertisement.objects.all().order_by("-created_at")
	recommendedProduct = ProductsManagement.objects.filter(recommended=True).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False))
	return render(request,'index.html',{"all_product_list":products,"offers":offers,"hot_items":hotItems,"advertisements":advertiseProducts,"recomended_product":recommendedProduct})

class SearchProduct(View):
	"""docstring for SearchProduct"""
	def post(self,request):
		params = request.POST
		current_date = datetime.now()
		product = ProductsManagement.objects.filter(Q(category__category_name__icontains=params['q']) | Q(subs_category__sub_category_name__icontains=params['q']) | Q(title__icontains=params['q'])).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False) | Q(recommended=True)).order_by('-created_at')
		offers = Offer.objects.filter(offer_end_date_time__gte=current_date.date())
		hotItems = OrderItems.objects.filter(product__expiry_date__gt=current_date.date()).distinct('product')
		advertiseProducts = Advertisement.objects.filter(Q(title__icontains=params['q'])).order_by("-created_at")
		recommendedProduct = ProductsManagement.objects.filter(recommended=True).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False))
		return render(request,'index.html',{"all_product_list":product,"offers":offers,"hot_items":hotItems,"advertisements":advertiseProducts,"recomended_product":recommendedProduct})

class Index(View):
	"""docstring for Index"""
	def get(self, request, slug=None):
		queryset = SubCategory.objects.all()
		print("Slug",slug)
		if slug:
			sub_category = get_object_or_404(queryset,slug=slug)
			sub_cat = ProductsManagement.objects.filter(subs_category__slug=slug)
			if sub_cat:
				return render(request, 'index.html', {'sub_cats':sub_cat})
			else:
				messages.info(request,"No product availabe for this category !")
				return redirect("Juntos:home")
		else:
			return redirect("Juntos:home")


class ProductImageView(View):
	"""docstring for ProductImageView"""
	
	def get(self, request,color=None):
		images = ProductImage.objects.filter(product_color_id=color).values('product_images')
		imagesArray = []
		for img in images:
			imagesArray.append(img['product_images'])
		return render(request, "partial-product-image-view.html",{"images":imagesArray})

class ProductColor(View):
	"""docstring for ProductColor"""
	
	def get(self, request):
		return render(request, 'product.html')
		
class ProceedCart(View):
	"""docstring for ProceedCart"""
	def get(self,request):
		user = request.user
		if user.is_authenticated and user.is_customer:
			total_price = 0.0
			product_cart = Cart.objects.filter(user=user)
			recomended_product = ProductsManagement.objects.filter(recommended=True).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False))[:3]
			if product_cart:
				total_price = product_cart.aggregate(Sum('price'))['price__sum']
				taxvalue = TaxPercentage.objects.first()
				address = ShippingAddress.objects.filter(user=request.user)
				grand_total = total_price + (total_price * int(taxvalue.tax))/100
				if address:
					address = address.latest('created_at')
					if address.mode_of_transport=="DHL":
						total_message = "exclusive shipping charge"
						pass
					else:
						grand_total = grand_total + int(5)
						total_message = "inclusive all"
				else:
					total_message = "exclusive shipping charge"
			else:
				total_price = 00.00
				grand_total = 00.00
				total_message = ""
			return render(request,'new_shipping_cart.html',{"all_cart":product_cart,"total_price":total_price,"grand_total":grand_total,"total_message":total_message,"recomended_product":recomended_product})

	def post(self,request):
		card_Array = []
		total_price = 0.0
		recomended_product = ProductsManagement.objects.filter(recommended=True).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False))[:3]
		if 'card_data' in request.POST and request.POST['card_data']:
			for items in ast.literal_eval(request.POST['card_data']):
				product = ProductsManagement.objects.get(id=items['product_id'])
				print(int(items['quantity']))
				card_Array.append({
					"product":product,
					"product_size":int(items['size']),
					"product_color": int(items['color']),
					"quantity": int(items['quantity']),
					"price": (product.selling_price if product.selling_price else product.price) * int(items['quantity'])
				})
				total_price = total_price + ((product.selling_price if product.selling_price else product.price) * int(items['quantity']))
			grand_total  = total_price + (total_price * 18)/100
			total_message = "exclusive shipping charge"
			return render(request, 'new_shipping_cart.html', {"all_cart":card_Array,"total_price":total_price,"grand_total":grand_total,"total_message":total_message,"recomended_product":recomended_product})


class WishList(View):
	"""docstring for WishList"""
	def get(self,request):
		if request.user.is_authenticated():
			user = request.user
			wishlist = Wishlist.objects.filter(user=user)
			return render(request, 'my_wishlist.html',{"lists":wishlist})
		else:
			return render(request, 'my_wishlist.html')

class AddWishList(View):
	"""docstring for AddWishList"""
	def get(self,request,pk=None):
		if request.user.is_customer:
			try:
				cartObj = Cart.objects.get(id=pk)
				product = ProductsManagement.objects.get(id=cartObj.product_id)
				Wishlist.objects.create(user=request.user, product=product)
				try:
					cartObj.delete()
					messages.success(request, "Cart Product successfully move to Wish List !")
					return redirect("Juntos:wish-list")
				except Exception as e:
					messages.error(request, "Something went wrong!")
					return redirect("Juntos:wish-list")
			except Exception as e:
				print("Exception in AddWhishlist",e)
				messages.error(request, "Cart Product does not exists !")
				return redirect("Juntos:views-cart")				
		else:
			messages.info(request, "Please login before access wishlist !")
			return redirect("Juntos:views-cart")

class RemoveWishList(View):
	"""docstring for RemoveWishList"""
	def get(self,request,pk=None):
		wishlistObj = Wishlist.objects.filter(id=pk)
		wishlistObj.delete()
		messages.success(request, "Item deleted in your whislist successfully")
		return redirect("Juntos:wish-list")
		
class FaqList(View):
	"""docstring for FaqList"""
	def get(self,request):
		faq = JuntosFAQs.objects.all()
		return render(request, 'faq.html',{"lists":faq})
			
class ConditionsView(View):
	"""docstring for ConditionsView"""
	def get(self,request):
		return render(request, 'conditions.html')

class TermsList(View):
	"""docstring for TermsList"""
	def get(self,request):
		JuntosTermConditions = JuntosTermCondition.objects.all()
		return render(request, 'terms.html',{"lists":JuntosTermConditions})

class CarrerList(View):
	"""docstring for ClassName"""
	def get(self,request):
		JuntosCareer = JuntosCareers.objects.all()
		return render(request, 'carrer.html',{"lists":JuntosCareer})

class ContactList(View):
	"""docstring for ClassName"""
	def get(self,request):
		JuntosContact = JuntosContactUs.objects.all()
		return render(request, 'contact-us.html',{"lists":JuntosContact})
														
class LoginView(View):
	"""docstring for LoginView"""
	def post(self,request):
		params = request.POST
		form = UserLoginForm(params, None)
		if form.is_valid():
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			user = authenticate(username=email, password=password)
			if user and user.is_superuser:
				login(request,user)
				return redirect('/Juntosadmin')
			if user and user.mobile_verified and user.confirmation_code=="Confirmed":
				login(request, user)
				if request.POST.get('card_data'):
					for items in ast.literal_eval(request.POST['card_data']):
						product = ProductsManagement.objects.get(id=items['product_id'])
						try:
							cart_exists = Cart.objects.get(product=product,user=user)
							cart_exists.product_size = int(items['size'])
							cart_exists.product_color = int(items['color'])
							cart_exists.quantity = int(items['quantity'])
							cart_exists.price = (product.selling_price if product.selling_price else product.price) * int(items['quantity'])
							cart_exists.save()
						except:
							Cart.objects.create(user=user, product=product,product_size=int(items['size']),product_color=int(items['color']),quantity=int(items['quantity']),price=(product.selling_price if product.selling_price else product.price) * int(items['quantity']))
				messages.success(request, "Login successfully.")
				return redirect('Juntos:home')
			elif user and not user.mobile_verified:
				request.session['email'] = user.email
				messages.success(request, "Your account confirmed successfully")
				return redirect('Juntos:resend_otp')
			elif user and not user.confirmation_code=="Not Confirmed":
				messages.success(request, "It seems that you are not activate your acccount via Email.Please click on the link send on your Registered Email to activate your Account.")
				request.session['email'] = user.email
				return redirect('Juntos:home')
			else:
				messages.error(request, "Authentication Failed.Please try again with valid Credentials.")
				return redirect('Juntos:home')
		else:
			return render(request,"index.html", {'forms':form})

class LogoutView(View):
	"""docstring for LogoutView"""
	def get(self,request):
		logout(request)
		return redirect('Juntos:home')


class RegisterView(View):
	"""docstring for RegisterView"""
	def post(self,request):
		params = request.POST
		form = UserRegistration(request.POST or None)
		if form.is_valid():
			user  = form.save(commit=False)
			user.confirmation_code = user.otp_creation()
			user.is_active   = False
			user.is_customer = True
			user.is_vendor   = False
			user.mobile_verification_code = user.otp_creation()
			user.set_password(params['password'])
			user.save()
			request.session['email'] = user.email
			user.otp_send()
			return render(request, 'resend_otp.html')
		else:
			return render(request, 'index.html', {'form': form})

# def send_mail(request):
#     if request.method == "POST":
#         form = ForgotSendCustomerForm(request.POST  or None)
#         if form.is_valid():
#             params = request.POST
#             user = Customer.objects.filter(email = params["email"]).first()
#             send_templated_mail(template_name='forgot_password',
#                               from_email=settings.EMAIL_HOST_USER,
#                               recipient_list=[user.email],
#                               context={'username': user.first_name,
#                                        'email': user.email,
#                                        'code': user.slug,
#                                        'activate': user.confirmation_code})
#             messages.info(request, "A new password link send to your given email address.")
#         else:
#             messages.error(request, "Email address does not exists !")
#     return redirect('Peru:home')
						
class SendMail(View):
	"""docstring for SendMail"""
	
	def get(self,request):
		return redirect('Peru:home')

class SubscribeNewsLetter(View):
	
	"""docstring for SubscribeNewsLetter"""
	def post(self,request):
		form = SubscribeNewsLetterForm(data=request.POST)
		if form.is_valid():
			form.save()
			return JsonResponse({"message":"You have subscribed for news letter", "status":200})
		return JsonResponse({"message":"You have already subscribed for this", "status":400})

class UpdateProfile(View):
	"""docstring for UpdateProfile"""
	def get(self,request):
		return render(request, "profile_update.html")
	def post(self,request):
		user = request.user
		params = request.POST
		form = ProfileForm(request.POST or None)
		if form.is_valid():
			user.first_name = params['first_name']
			user.mobile = params['mobile']
			user.save()
		return render(request, 'profile_update.html')


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

class ViewOrder(View):
	"""docstring for ViewOrder"""
	def get(self,request):
		orders = OrderItems.objects.filter(order__customer=request.user,order_cancel_request=False)
		return render(request, 'orders.html', {'orders':orders})
	def post(self,request):
		return render(request, 'orders.html')

class CheckOTP(View):
	"""docstring for CheckOTP"""
	def post(self,request):
		queryset = MyUser.objects.all()
		params = request.POST
		email = request.session['email']
		user   = get_object_or_404(queryset,email=email)
		if user.mobile_verification_code == params['mobile_otp']:
			user.mobile_verified = True
			user.save()
			user.successfull()
			messages.info(request, 'To activate your account click on link send on your registered email.')
			messages.success(request, 'Your mobile number verified successfully.')
			del request.session['email']
			user.send_mail_activation()
			return redirect('Juntos:home')
		else:
			messages.error(request, 'Please enter valid OTP !')
			return render(request, 'resend_otp.html')

class ResendOTP(View):
	"""docstring for ResendOTP"""
	def get(self,request):
		queryset = MyUser.objeects.all()
		email = request.session['email']
		if email:
			user = get_object_or_404(queryset,email=email)
			user.mobile_verification_code = user.otp_creation()
			user.save()
			user.otp_send()
			messages.success(request, 'A new OTP send on your registered number.')
			return render(request, 'resend_otp.html')
		else:
			messages.error(request, 'Session expired !')
			return render(request, 'otp_screen.html')


class ConfirmationEmail(View):
	"""docstring for ConfirmationEmail"""
	def get(self,request,confirmation_code=None):
		queryset = MyUser.objects.all()
		user = get_object_or_404(queryset,confirmation_code=confirmation_code)
		user.is_active = True
		user.confirmation_code = "Confirmed"
		user.save()
		messages.success(request, "Your account confirmed successfully")
		return redirect("Juntos:home")

class ProductDetail(View):
	"""docstring for ProductDetail"""
	def get(self,request,slug=None):
		queryset = ProductsManagement.objects.all()
		product = get_object_or_404(queryset,slug=slug)
		relatedProducts = ProductsManagement.objects.filter(subs_category=product.subs_category).exclude(id=product.id).exclude(Q(expiry_date__lt=datetime.now()) | Q(expiry_date__isnull=True) | Q(product_quantity=0) | Q(is_active=False))[:5]
		return render(request, 'product.html',{"details":product,"related_products":relatedProducts})	


class ViewCart(View):
	"""docstring for ViewCart"""
	def get(self,request):
		user = request.user
		if user.is_authenticated and user.is_customer:
			total_price = 0.0
			product_cart = Cart.objects.filter(user=user)
			total_price = product_cart.aggregate(Sum('price'))['price__sum']
			total_price = total_price + (total_price * 18)/100
			return render(request,'new_view_cart.html',{"all_cart":product_cart,"total_price":total_price})
	def post(self,request):
		user = request.user
		if user.is_authenticated and user.is_customer:
			total_price = 0
			product_cart = Cart.objects.filter(user=user)
			total_price = product_cart.aggregate(Sum('price'))['price__sum']
			total_price = total_price + (float(total_price) * 18)/100
			return render(request,'new_view_cart.html',{"all_cart":product_cart,"total_price":total_price})
		else:
			card_Array = []
			total_price = 0.0
			print(request.POST['card_data'])
			if 'card_data' in request.POST and request.POST['card_data']:
				for items in ast.literal_eval(request.POST['card_data']):
					product = ProductsManagement.objects.get(id=int(items['product_id']))
					card_Array.append({
						"product":product,
						"product_size":int(items['size']),
						"product_color": int(items['color']),
						"quantity": int(items['quantity']),
						"price": (product.selling_price if product.selling_price else product.price) * int(items['quantity'])
					})
					total_price = total_price + (product.selling_price if product.selling_price else product.price) * int(items['quantity'])
				return render(request, 'new_view_cart.html', {"all_cart":card_Array,"total_price":total_price})

class CheckAvailability(View):
	"""docstring for CheckAvailability"""
	def post(self,request):
		params = request.POST
		try:
			quantity = ProductsManagement.objects.get(id=params["product"])
			return HttpResponse(json.dumps({"message": "Success", "quantity":quantity.product_quantity, "code":200}), content_type='application/json')
		except:
			return HttpResponse(json.dumps({"message": "Product not found","code":404}), content_type='application/json')


# def helpfull_review(request):
#     try:
#         review = Customer_Review.objects.get(id=request.POST['review'])
#         HelpFullReviews.objects.create(customer=request.user, review=review)
#         return HttpResponse(json.dumps({"status": True}), content_type='application/json')
#     except:
#         return HttpResponse(json.dumps({"status": False}), content_type='application/json')									
class HelpfullReview(View):
	"""docstring for HelpfullReview"""
	def get(self,request):
		return HttpResponse(json.dumps({"status": False}), content_type='application/json')

class CustomerReviewView(View):
	"""docstring for CustomerReview"""
	def post(self,request):
		params = request.POST
		review = CustomerReview.objects.create(product_id=params['product'],content=params['content'],rating=params['rating_value'],user=request.user)
		total_review  = CustomerReview.objects.all().count()
		return redirect("Juntos:product-detail", params['slug'])
		
class AddToCart(View):
	"""docstring for AddToCart"""
	def post(self,request):
		params = request.POST
		user = request.user
		try:
			product_obj = ProductsManagement.objects.get(id=params['product_id'])
			price_on_cart = (product_obj.selling_price if product_obj.selling_price else product_obj.price)*int(params['quantity'])
			try:
				product_card = Cart.objects.get(product=product_obj, user=user)
				product_card.quantity = params['quantity']
				product_card.product_size = params.get('size',product_card.product_size)
				product_card.product_color = params.get('color',product_card.product_color)
				product_card.price = price_on_cart
				product_card.save()
			except Exception as e:
				card = Cart(user=user, active=True, product=product_obj)
				card.quantity=params['quantity']
				card.product_size=params.get('size',None)
				card.product_color=params.get('color',None)
				card.price=price_on_cart
				card.save()
			return HttpResponse(json.dumps({"code":200}), content_type='application/json')
		except Exception as e:
			return HttpResponse(json.dumps({"code":500}), content_type='application/json')

class AddShipping(View):
	"""docstring for AddShipping"""
	def post(self,request):
		if request.user.is_authenticated() and request.user.is_customer:
			b_form = BillingForm(request.POST or None)
			s_form = ShippingForm(request.POST or None)
			if b_form.is_valid() and s_form.is_valid():
				b_form.save()
				s_form.save()
				messages.success(request, "Shipping address saved successfully")
				return redirect('Juntos:customer-order-summary')
			else:
				return render(request, 'shipping_billing.html',{"s_form":s_form,"b_form":b_form})
		else:
			messages.info(request, "Before you place your order! Please Sign In First.")
			return render(request, 'new_shipping_cart.html')

	def get(self,request):
		shipping = ShippingAddress.objects.filter(user=request.user)
		if request.user.is_authenticated() and request.user.is_customer and shipping:
			return redirect("Juntos:customer-order-summary")
		else:
			return render(request, 'shipping_billing.html')


class AddAnotherShipping(View):
	"""docstring for AddShipping"""
	def post(self,request):
		if request.user.is_authenticated() and request.user.is_customer:
			b_form = BillingForm(request.POST or None)
			s_form = ShippingForm(request.POST or None)
			if b_form.is_valid() and s_form.is_valid():
				b_form.save()
				s_form.save()
				messages.success(request, "Shipping address saved successfully")
				return redirect('Juntos:customer-order-summary')
			else:
				return render(request, 'shipping_billing.html',{"s_form":s_form,"b_form":b_form})
		else:
			messages.info(request, "Before you place your order! Please Sign In First.")
			return render(request, 'new_shipping_cart.html')

	def get(self,request):
		return render(request, 'shipping_billing.html')



class CustomerOrderSummary(View):
	"""docstring for CustomerOrderSummary"""
	def get(self,request):
		if request.user.is_customer:
			return render(request, "order-summary.html")
		else:
			messages.info(request, "You are not authorize to access this page.")
			return redirect("Juntos:home")

def create_order(user, payment_type, shiping_address):
	cart = Cart.objects.filter(user=user)
	base_price = 00.00
	for c in cart:
		base_price = base_price + (c.quantity*c.price)
	tax_percent = TaxPercentage.objects.first().tax
	tax_charges = (base_price*tax_percent)/100
	if shiping_address.mode_of_transport=="GPS":
		shipping_percent = 0
		shipping_charge = 5
	else:
		shipping_percent = 5
		shipping_charge = (base_price*5)/100

	total_price = base_price+shipping_charge+tax_charges
	order = CustomerOrder.objects.create(shipping_address=shiping_address,customer=user,order_payment_type=payment_type,delivery_date=(datetime.today()+timedelta(days=8)).date(),base_price=base_price,shipping_percent=shipping_percent,shipping_charge=shipping_charge,tax_percent=tax_percent,tax_charges=tax_charges,total=total_price)
	send_place_order_customer(order,cart)
	send_place_order_admin(order,cart)
	order_items(cart,order,shiping_address)

def order_items(cart,order,address):
	for obj in cart:
		if address.mode_of_transport=="GPS":
			shipping_percent = 0
			shipping_charge = 5
		else:
			shipping_percent = 5
			shipping_charge = (obj.price*obj.quantity*5)/100
		tax_percent = TaxPercentage.objects.first().tax
		tax_charges = (obj.price*obj.quantity*tax_percent)/100
		total_price = (obj.price*obj.quantity)+shipping_charge+tax_charges
		OrderItems.objects.create(order=order,product=obj.product,product_color=obj.product_color,product_size=obj.product_size,quantity=obj.quantity,base_price=obj.price*obj.quantity,shipping_percent=shipping_percent,shipping_charge=shipping_charge,tax_percent=tax_percent,tax_charges=tax_charges,total=total_price)
		obj.product.product_quantity = obj.product.product_quantity - obj.quantity
		obj.product.save()
		send_place_order_vendor(obj)
		obj.delete()
		# product = ProductsManagement.objects.get(id=obj.product.id)
		# product.product_quantity = product.product_quantity - obj.quantity
		# product.save()
		# Cart.objects.get(id=obj.id).delete()
		message = "Congrats, A New Order has been received for '"+obj.product.subs_category.sub_category_name+"' types product."
		notification = Notifications.objects.create(vendor=obj.product.vendor, ntype=1, content=message)
		notification_data = {}
		notification_data['content'] = notification.content
		notification_data['ntype']   = notification.ntype
		notification_data['vendor']  = notification.vendor.id
		# send_notification_task.delay(notification_data)

def send_place_order_vendor(cartObj):
	send_templated_mail(
		template_name='checkoutVendor',
		from_email=settings.EMAIL_HOST_USER,
		auth_user=settings.EMAIL_HOST_USER,
		auth_password=settings.EMAIL_HOST_PASSWORD,
		recipient_list=[cartObj.product.vendor.email],
		# recipient_list=["imtiyaz.ahemad@mobiloittegroup.com"],
		context={
			"obj":cartObj
	})

def send_place_order_customer(orderObj,cartObj):
	send_templated_mail(
		template_name='checkoutCustomer',
		from_email=settings.EMAIL_HOST_USER,
		auth_user=settings.EMAIL_HOST_USER,
		auth_password=settings.EMAIL_HOST_PASSWORD,
		recipient_list=[orderObj.customer.email],
		# recipient_list=["imtiyaz.ahemad@mobiloittegroup.com"],
		context={
			"order":orderObj,
			"cart":cartObj
	})

def send_place_order_admin(orderObj,cartObj):
	send_templated_mail(template_name='checkoutAdmin',
		from_email=settings.EMAIL_HOST_USER,
		auth_user=settings.EMAIL_HOST_USER,
		auth_password=settings.EMAIL_HOST_PASSWORD,
		recipient_list=["imtiyaz.ahemad@mobiloittegroup.com"],
		context={
			"order":orderObj,
			"cart":cartObj
	})

class OrderPayment(View):
	"""docstring for OrderPayment"""

	def get(self,request):
		user = request.user
		return render(request, "payment.html")

	def post(self,request):
		user = request.user
		shipping_address = user.shiping_address.latest('created_at')
		if shipping_address:
			cartObj = Cart.objects.filter(user=user)
			tax = TaxPercentage.objects.first()
			user_data = []
			admin_commission = 0
			for cart in cartObj:
				if not any(vendor.get('email') == cart.product.vendor.email for vendor in user_data):
					total_pay = cartObj.filter(product__vendor__email=cart.product.vendor.email).aggregate(Sum('price'))['price__sum']
					taxPrice = (total_pay*(tax.tax))/100
					total_payment = taxPrice + total_pay
					if shipping_address.mode_of_transport=="DHL":
						pass
					else:
						total_payment = total_payment + int(5)
					price = total_payment - cart.price*5/100
					user_data.append({"email":cart.product.vendor.email, "amount": float(price)})
				admin_commission +=  cart.price*5/100
			response_url =  payment(user_data, admin_commission, user)
			if 'ack' in response_url and response_url['ack']=="Success":
				return redirect(response_url['url'])
			else:
				messages.error(request, response_url['error'][0]['message'])
				return render(request, "payment.html",{"errorId":response_url['error'][0]['errorId']})
		else:
			messages.error(request, "Please select your order shiping address")
			return redirect("Juntos:add-shipping")

class CODOrder(View):
	"""docstring for CODOrder"""
	def get(self,request):
		if request.user.is_customer:
			address = ShippingAddress.objects.filter(user=request.user).latest('created_at')
			if address:
				create_order(request.user,"COD",address)
				return redirect("Juntos:order-placed")
		else:
			messages.error(request, "You are not authenticated to access this page.")
			return redirect("Juntos:home")


@login_required(login_url="/")
def order_placed(request):
    user_detail = request.user
    address = Shipping_Address.objects.filter(user=user_detail).last()
    order_detail = CustomerOrder.objects.filter(customer=user_detail).last()
    quantiy_handle = CustomerOrder_items.objects.filter(order_id=order_detail.id)
    for p in quantiy_handle:
        product = Products_Management.objects.get(id=p.product.id)
        product.product_quantity = product.product_quantity-p.quantity
        if product.product_quantity < 1:
            product.product_quantity = 0
            product.in_stock = False
            product.save()
        else:
            product.in_stock = True
            product.save()
    b = CustomerOrder_items.objects.filter(order_id=order_detail)
    return render(request, "order_confirmation_page.html",{"address":address,"order_detail":order_detail,"b":b[0].product})	

class OrderPlaced(View):
	"""docstring for OrderPlaced"""
	def get(self,request):
		Cart.objects.filter(user=request.user).delete()
		last_order = CustomerOrder.objects.filter(customer=request.user).latest('created_at')
		order_items = last_order.order_items.all()
		billing_details = BillingAddress.objects.filter(user=request.user).latest('created_at')
		return render(request, "order_confirmation_page.html",{"last_order":last_order,"order_items":order_items,'billing_details':billing_details})	

# class DhlShippingPrice(View):
# 	"""docstring for DhlShippingPrice"""
# 	def get(self,request):
# 		total_shipping_charges = 0.0
# 		for pro in product_cart:
# 			try:
# 				v_details = Vendor_Account_Details.objects.get(vendor = pro.product.vendor.id)
# 				product_ship_detail = Products_Management.objects.get(id=pro.product.id)
# 				total_shipping_charges = total_shipping_charges + dhl_charges.ship(v_details,product_ship_detail)
# 			except Exception as e:
# 				total_shipping_charges = total_shipping_charges + pro.price
# 				grand_total = (total_shipping_charges*23)/100
# 				charges_amount = grand_total + total_shipping_charges
# 				total_amount = charges_amount
# 		return HttpResponse(json.dumps({"total_shipping_charges": total_amount}), content_type='application/json')

# @login_required(login_url="/")
# def customer_review(request):
#     params = request.POST
#     slug = params['slug']
#     review = Customer_Review.objects.create(product_id=params['product'],
#                                              content=params['content'],
#                                              rating_value=params['rating_value'],
#                                              given_by=request.user)
#     total_review  = Customer_Review.objects.all().count()
#     return redirect("Peru:product_detail", slug)

class Rating(View):
	"""docstring for Rating"""
	def post(self,request):
		params = request.POST
		return redirect("Juntos:product-detail", params['slug'])

class IncreaseCartQuantity(View):
	"""docstring for IncreaseCartQuantity"""
	def post(self,request):
	    params = request.POST
	    cart = Cart.objects.get(id=params['product_id'])
	    price = cart.product.selling_price * int(params['quantity'])
	    cart.quantity = params['quantity']
	    cart.price    = price
	    cart.save()
	    return HttpResponse(json.dumps({"code":200}), content_type='application/json')
																																																																																																																																																																																																																																																																																																																													
class RemoveFromCart(View):
	"""docstring for RemoveFromCart"""
	def get(self,request,pk=None):
	    user = request.user
	    if user.is_authenticated:
	        cart = Cart.objects.filter(product_id=pk,user=request.user)
	        cart.active = False
	        cart.delete()
	        messages.success(request,"Item deleted successfully from your cart")
	        return redirect("Juntos:proceed-cart")
	    else:
	        return redirect("customer:proceed_cart")

class AddWhishlist(View):
	"""docstring for AddWhishlist"""
	def get(self,request,pk=None):
		if request.user.is_customer:
			try:
				cartObj = Cart.objects.get(id=pk)
				product = ProductsManagement.objects.get(id=cartObj.product_id)
				Wishlist.objects.create(user=request.user, product=product)
				try:
					cartObj.delete()
					messages.success(request, "Cart Product successfully move to Wish List !")
					return redirect("Juntos:wish-list")
				except Exception as e:
					messages.error(request, "Something went wrong!")
					return redirect("Juntos:wish-list")
			except Exception as e:
				print("Exception in AddWhishlist",e)
				messages.error(request, "Cart Product does not exists !")
				return redirect("Juntos:views-cart")				
		else:
			messages.info(request, "Please login before access wishlist !")
			return redirect("Juntos:views-cart")


class CancelOrderAndRefund(View):
	"""docstring for CancelOrderAndRefund"""
	def get(self,request,order=None):
		order_obj = OrderItems.objects.get(id=order)
		message = "Order cancel request for Order number: #"+str(order_obj.order_number)+", for product SKU #"+str(order_obj.product.subs_category.sub_category_name)+" received."
		Notifications.objects.create(vendor=order_obj.product.vendor,ntype="Order Cancel Request.",content=message)
		order_obj.product.product_quantity = order_obj.product.product_quantity + order_obj.quantity
		order_obj.product.save()
		order_obj.order_cancel_request = True
		order_obj.save()
		return redirect("Juntos:view-order")

class Recommended(View):
	"""docstring for Recommended"""
	def get(self,request):
		all_recommendeds = Advertisement.objects.filter(recommended=True)
		if all_recommendeds.exists():
			paginator = Paginator(all_recommendeds, 12)
			all_category=Category.objects.all()
			index=1
			page = request.GET.get('page')
			try:
				all_recommendeds = paginator.page(page)
			except PageNotAnInteger:
				all_recommendeds = paginator.page(1)
			except EmptyPage:
				all_recommendeds = paginator.page(paginator.num_pages)
				return render (request, 'index.html',{"all_recommendeds":all_recommendeds})
		else:
			messages.info(request,"No recommended avaialable")
			return redirect("Juntos:home")

class AdvertisementDetail(View):
	"""docstring for AdvertisementDetail"""
	def get(self,request,slug=None,tx=None,amt=None):
		sb_ct= SubCategory.objects.filter(sub_category_tag="VP")
		advertisement = Advertisement.objects.get(slug=slug)
		# total_review = advertisement.reviews_adv.all()
		related_services = Advertisement.objects.filter(type_of_services=advertisement.type_of_services,location=advertisement.location).exclude(slug=slug)
		return render(request, 'detail_advertisement.html', {'ads_details':advertisement, 'related_services':related_services,'res_cat':sb_ct})


class AdvertismentsReview(View):
	"""docstring for AdvertismentsReview"""
	def post(self,request):
		params = request.POST
		slug = params['slug']
		adv = Advertisement.objects.get(id=params['advertisement_reviews'])
		review = AdvertismentReview.objects.create(advertisement_reviews=adv,content=params['content'],rating=params['rating_value'],user=request.user)
		return redirect("Juntos:advertisment-detail", slug)

	
# @login_required(login_url="/")
# def paypal_order_placed(request):
#     customer = request.user
#     transaction = CustomerTransactionDetails.objects.filter(customer=customer).last()
#     payment_details =  ast.literal_eval(paypal_payment_details(transaction.pay_key).decode("utf-8"))
#     # print(payment_details)
#     if payment_details['status'] == 'COMPLETED':
#         shiping_address = customer.shiping_address.filter(selected=True).last()  ##  find shiping address
#         order = create_order_and_order_item_record(customer, "Paypal", shiping_address)
#         for detail in payment_details['paymentInfoList']['paymentInfo']:
#             transaction.order_id = order
#             transaction.customer=customer
#             transaction.payment_status = payment_details['status']
#             transaction.sender_email=payment_details['sender']['email']
#             transaction.sender_account_id=payment_details['sender']['accountId']
#             transaction.tranaction_status = detail['senderTransactionStatus']
#             transaction.tranaction_id = detail['senderTransactionId']
#             # transaction.payment_refunded_ammount = detail['refundedAmount']
#             transaction.reciever_account_id = detail['receiver']['accountId']
#             transaction.reciever_email = detail['receiver']['email']
#             transaction.reciever_amount = detail['receiver']['amount']
#             transaction.save()
#         messages.success(request, "Your order placed successfully.")
#         return redirect('customer:order_placed')
#     else:
#         messages.error(request, "Payment Failed, Unable to placed your order!")
#         return redirect('customer:order_cancel')



class OrderCancel(View):
	"""docstring for ClassName"""
	def get(self,request):
	    Cart.objects.filter(user=request.user).delete()
	    customer = request.user
	    transaction = CustomerTransactionDetails.objects.filter(customer=customer).latest('created_at')
	    return render(request, "order-canceled.html")

class PaypalOrderPlaced(View):
	"""docstring for PaypalOrderPlaced"""
	def get(self,request):
		customer = request.user
		transaction = CustomerTransactionDetails.objects.filter(customer=customer).latest('created_at')
		payment_details =  ast.literal_eval(paypal_payment_details(transaction.pay_key).decode("utf-8"))
		if payment_details['status'] == 'COMPLETED':
		    shiping_address = customer.shiping_address.latest('created_at')  ##  find shiping address
		    order = create_order(customer, "Paypal", shiping_address)
		    for detail in payment_details['paymentInfoList']['paymentInfo']:
		        transaction.order_id = order
		        transaction.customer=customer
		        transaction.payment_status = payment_details['status']
		        transaction.sender_email=payment_details['sender']['email']
		        transaction.sender_account_id=payment_details['sender']['accountId']
		        transaction.tranaction_status = detail['senderTransactionStatus']
		        transaction.tranaction_id = detail['senderTransactionId']
		        transaction.reciever_account_id = detail['receiver']['accountId']
		        transaction.reciever_email = detail['receiver']['email']
		        transaction.reciever_amount = detail['receiver']['amount']
		        transaction.save()
		    messages.success(request, "Your order placed successfully.")
		    return redirect('Juntos:order-placed')
		else:
		    messages.error(request, "Payment Failed, Unable to placed your order!")
		    return redirect('Juntos:order-cancel')
	def post(self,request):
		customer = request.user
		transaction = CustomerTransactionDetails.objects.filter(customer=customer).latest('created_at')
		payment_details =  ast.literal_eval(paypal_payment_details(transaction.pay_key).decode("utf-8"))
		if payment_details['status'] == 'COMPLETED':
			shiping_address = customer.shiping_address.latest('created_at')  ##  find shiping address
			order = create_order(customer, "Paypal", shiping_address)
			for detail in payment_details['paymentInfoList']['paymentInfo']:
			    transaction.order_id = order
			    transaction.customer=customer
			    transaction.payment_status = payment_details['status']
			    transaction.sender_email=payment_details['sender']['email']
			    transaction.sender_account_id=payment_details['sender']['accountId']
			    transaction.tranaction_status = detail['senderTransactionStatus']
			    transaction.tranaction_id = detail['senderTransactionId']
			    transaction.reciever_account_id = detail['receiver']['accountId']
			    transaction.reciever_email = detail['receiver']['email']
			    transaction.reciever_amount = detail['receiver']['amount']
			    transaction.save()
			messages.success(request, "Your order placed successfully.")
			return redirect('Juntos:order-placed')
		else:
			messages.error(request, "Payment Failed, Unable to placed your order!")
			return redirect('Juntos:order-cancel')
	

class ContactUsEmail(View):
	"""docstring for ContactUsEmail"""
	def post(self,request):
		from django.template import loader
		form = JuntosContactUsEmailForm(data=request.POST)
		if form.is_valid():
			form.save()
			return JsonResponse({"status":200,"message":"Your request save will contact you soon."})
		return JsonResponse({"status":400,"message":"Something went wrong."})

																				
														