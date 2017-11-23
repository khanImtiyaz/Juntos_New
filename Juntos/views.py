from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
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
from Static_Model.models import *

# Create your views here.

def landingpage(request):
    hot_items = []
    hot_deals = CustomerOrder_items.objects.values("product_id").annotate(Count("product_id")).order_by("-product_id__count")[:5]
    for deal in hot_deals:
        prod = Products_Management.objects.get(id=deal['product_id'])
        hot_items.append({'title':prod.title,"id":prod.id ,"slug":prod.slug,"selling_price":prod.selling_price,"image":prod.image.name,"sub_cat_tag":prod.subs_category.sub_category_tag})
    offers = Offer.objects.all()
    if request.GET.get('all',None):
        banner = Banner.objects.all()
        product_list = Products_Management.objects.all().exclude(expire_products=0)
        paginator = Paginator(product_list, 12)
        all_category=Category.objects.all()
        index=1
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = ({'all_product_list': products, "categorys":all_category, 'banner_list':banner, "hot_items":hot_items, "offers":offers})
        response_data = render(request,"index.html",context)
        if not request.COOKIES.get('add_card_token') and not request.user.is_authenticated():
            import uuid
            token =  uuid.uuid4().hex[:16].upper()
            response_data.set_cookie('add_card_token', token)
        return response_data
    else:
        recomended_product = Advertisement.objects.filter(recommended=True).order_by("-created_at")[:4]
        banner = Banner.objects.all()
        product_list = Products_Management.objects.all().order_by("-created_at").exclude(expire_products=0)
        paginator = Paginator(product_list, 8)
        all_category=Category.objects.all()
        index=1
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = ({'product_list': products, "categorys":all_category, 'banner_list':banner, "recomended_product":recomended_product, "hot_items":hot_items,"offers":offers})
        response_data = render(request,"index.html",context)
        if not request.COOKIES.get('add_card_token') and not request.user.is_authenticated():
            import uuid
            token =  uuid.uuid4().hex[:16].upper()
            response_data.set_cookie('add_card_token', token)
        return response_data

def home(request):
	product = ProductsManagement.objects.all().exclude(Q(expire_products=0) | Q(product_quantity=0) | Q(is_active=False) | Q(recommended=True))
	offers = Offer.objects.all()
	hotItems = OrderItems.objects.all().distinct('product')
	advertiseProducts = Advertisement.objects.filter(recommended=True).order_by("-created_at")[:4]
	recommendedProduct = ProductsManagement.objects.filter(recommended=True).exclude(Q(expire_products=0) | Q(product_quantity=0) | Q(is_active=False))
	return render(request,'index.html',{"all_product_list":product,"offers":offers,"hot_items":hotItems,"advertisements":advertiseProducts,"recomended_product":recommendedProduct})

# def product_detail(request, slug=None):
#     # try:
#     detail = Products_Management.objects.filter(slug=slug).first()
#     product_color = detail.product_colors
#     product_rating = detail.product_reviews.aggregate(Avg('rating_value'))['rating_value__avg']
#     if not product_rating:
#         product_rating = 0
#     total_review = detail.product_reviews.all()
#     # print(total_review)
#     seller = detail.vendor.first_name
#     if product_color.exists():
#         if request.GET.get('color',None):
#             try:
#                 product_images = product_color.get(id=request.GET.get('color')).product_color_images.values()
#             except:
#                 product_images = product_color.last().product_color_images.values()
#         else:
#             product_images = product_color.last().product_color_images.values()
#     else:
#         product_images = None
#     related_products = detail.subs_category.sub_cat_product.filter(selling_price__lte=detail.selling_price).exclude(id=detail.id)[:5]
#     # print(detail.subs_category.sub_category_flage)
#     context =  {'details':detail,
#                 'colors':product_color,
#                 "images":product_images,
#                 "total_review":total_review,
#                 "flage": True if detail.subs_category.sub_category_flage=="CLOTH"  else False ,
#                 "related_products":related_products,
#                 'seller':seller,
#                 'rating_comp':int(product_rating),
#                 'loop_count':range(1,6)}
#     return render(request, 'product.html',context)


		
# def product_image_view(request, color):
#     images = Product_Image.objects.filter(product_colr_id=color)
#     return render(request, "partial-product_image_view.html",{"images":images})

class ProductImageView(View):
	"""docstring for ProductImageView"""
	
	def get(self, request,color=None):
		images = ProductImage.objects.filter(product_color_id=color).values('product_images')
		imagesArray = []
		for img in images:
			imagesArray.append(img['product_images'])
		return render(request, "partial-product_image_view.html",{"images":imagesArray})

# def search_product(request):
#     return render(request,"index.html",{})

class SearchProduct(View):
	"""docstring for SearchProduct"""
	
	def get(self, request):
		return render(request,"index.html")

# def product_color(request, pk=None):
#     return render(request, 'product.html', {})

class ProductColor(View):
	"""docstring for ProductColor"""
	
	def get(self, request):
		return render(request, 'product.html')
		

# @register.filter
# def index(request, slug=None):
#     if slug:
#         sub_cat = Sub_Category.objects.filter(slug=slug).first()
#         if sub_cat:
#             # print("if")
#             try:
#                 advertisement = sub_cat.sub_advertisments.all()
#             except Exception as e:
#                 print("Error----",e)
#                 advertisement = {}
#         sb_ct = Sub_Category.objects.filter(sub_category_tag="VP")
#         #paginator = Paginator(user_list, 8)
#         all_sub = sub_cat.sub_cat_product.values()
#         paginator = Paginator(all_sub, 12)
#         banner = Banner.objects.all()
#         all_category=Category.objects.all()
#         offers = Offer.objects.all()
#         hot_items = []
#         hot_deals = CustomerOrder_items.objects.values("product_id").annotate(Count("product_id")).order_by("-product_id__count")[:5]
#         for deal in hot_deals:
#             prod = Products_Management.objects.get(id=deal['product_id'])
#             hot_items.append({'title':prod.title,"id":prod.id,"slug":prod.slug,"selling_price":prod.selling_price,"image":prod.image.name,"sub_cat_tag":prod.subs_category.sub_category_tag})
#         #print(hot_items)
#         page = request.GET.get('page')
#         try:
#             contacts = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             contacts = paginator.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             contacts = paginator.page(paginator.num_pages)
#         # or advertisement.exists()
#         if all_sub.exists()  or sb_ct.exists():
#             return render(request, 'index.html', {'sub_cats':all_sub, "hot_items":hot_items ,"offers":offers,"categorys":all_category, 'banner_list':banner,"header_name":sub_cat.sub_category_name,'advertisements':advertisement, 'contacts': contacts,'res_cat':sb_ct})
#         else:
#             messages.info(request,"No product availabe for this category !")
#             return redirect("Peru:home")
#     else:
#         return redirect("Peru:home")

class Index(View):
	"""docstring for Index"""
	def get(self, request, slug=None):
		queryset = SubCategory.objects.all()
		if slug:
			sub_category = get_object_or_404(queryset,slug=slug)
			sub_cat = ProductsManagement.objects.filter(subs_category=sub_category.id)
			if sub_cat:
				return render(request, 'index.html', {'sub_cats':sub_cat})
			else:
				messages.info(request,"No product availabe for this category !")
				return redirect("Juntos:home")
		else:
			return redirect("Juntos:home")

class ProceedCart(View):
	"""docstring for ProceedCart"""
	def get(self,request):
		user = request.user
		if user.is_authenticated and user.is_customer:
			total_price = 0.0
			product_cart = Cart.objects.filter(user=user)
			recomended_product = ProductsManagement.objects.filter(recommended=True).order_by("-created_at")[:3]
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
			return render(request,'new_shipping_cart.html',{"all_cart":product_cart,"total_price":total_price,"grand_total":grand_total,"total_message":total_message,"recomended_product":recomended_product})

	def post(self,request):
		card_Array = []
		total_price = 0.0
		recomended_product = ProductsManagement.objects.filter(recommended=True).order_by("-created_at")[:3]
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


# @login_required(login_url="/")
# def wish_list(request):
#     if request.user.is_authenticated():
#         user = request.user
#         detail_wishlist = Wishlist.objects.filter(user_id=user)
#         # messages.success(request, "Wishlist Item Remove Succesfully")
#         return render(request, 'my_wishlist.html',{"lists":detail_wishlist})
#     else:
#         return render(request, 'my_wishlist.html')

class WishList(View):
	"""docstring for WishList"""
	def get(self,request):
		if request.user.is_authenticated():
			user = request.user
			wishlist = Wishlist.objects.filter(user=user)
			return render(request, 'my_wishlist.html',{"lists":wishlist})
		else:
			return render(request, 'my_wishlist.html')

# @login_required(login_url="/")
def add_whishlist(request , product_id):
    if request.user.is_customer:
        product_obj = Products_Management.objects.filter(id=product_id)
        if product_obj.exists():
            product = product_obj.first()
            Wishlist.objects.create(user=request.user, product=product)
            try:
                Cart.objects.get(product=product).delete()
            except Exception as e:
                print (e)
            # Cart.objects.get(product=product).delete()
            return redirect("customer:wish_list")
        else:
            messages.error(request, "Product does not exists !")
            return redirect("customer:views_cart")
    else:
        messages.info(request, "Please login before access wishlist !")
        return redirect("customer:views_cart")


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
		return render(request, 'contact_us.html',{"lists":JuntosContact})
														
# def login_view(request):
#     redirect_to = request.POST.get('next', request.GET.get('next', ''))
#     if request.method=='POST':
#         product   = Products_Management.objects.all()
#         paginator = Paginator(product, 10)

#         all_category = Category.objects.all()
#         index=1
#         page = request.GET.get('page')
#         try:
#             contacts = paginator.page(page)
#         except PageNotAnInteger:
#             contacts = paginator.page(1)
#         except EmptyPage:
#             contacts = paginator.page(paginator.num_pages)
#         form = UserLoginForm(request.POST, None)
#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password"]
#             try:
#                 user = Customer.objects.get(email=email)
#                 user = authenticate(username=user.email, password=password)
#                 if not user.mobile_verified:
#                     request.session['email'] = user.email
#                     return redirect('customer:resend_otp')
#                 else:
#                     login(request, user)
#                 if request.POST.get('card_data'):
#                     """ Add all cart item in Cart after login"""
#                     for items in ast.literal_eval(request.POST['card_data']):
#                         product = Products_Management.objects.get(id=items['product_id'])
#                         card = Cart.objects.filter(user_id=user.id, product_id=items['product_id'])
#                         print("Card",card)
#                         if card.count()==1:
#                             cart = Cart.objects.get(user_id=user.id, product_id=items['product_id'])
#                             cart.product_size = int(items['size'])
#                             cart.product_color = int(items['color'])
#                             cart.quantity = int(items['quantity'])
#                             cart.price = product.price * int(items['quantity'])
#                             cart.save()
#                         else:
#                             cart1 = Cart(user_id=user.id, product_id=items['product_id'])
#                             cart1.product_size = int(items['size'])
#                             cart1.product_color = int(items['color'])
#                             cart1.quantity = int(items['quantity'])
#                             cart1.price = product.price * int(items['quantity'])
#                             cart1.save()
#                 total_cart = user.card_user.count()
#                 messages.success(request, "Login successfully.")
#                 try:
#                     remember = request.POST.get('remember_me')
#                     if remember:
#                         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#                 except MultiValueDictKeyError:
#                     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#                 responss = redirect(redirect_to)
#                 responss.delete_cookie('add_card_token')
#                 if redirect_to and is_safe_url(url=redirect_to, host=request.get_host()):
#                     return redirect(redirect_to)
#                 else:
#                     return redirect("Peru:home")
#             except:
#                 return redirect('Peru:home')
#         else:
#             return render(request,"index.html", {'forms':form,"categorys":all_category, "product_list":contacts})
#     else:
#         return redirect('Peru:home')

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


# @csrf_exempt
# def register_view(request):
#     user_list = Products_Management.objects.all()
#     hot_items = []
#     hot_deals = CustomerOrder_items.objects.values("product_id").annotate(Count("product_id")).order_by("-product_id__count")[:5]
#     for deal in hot_deals:
#         prod = Products_Management.objects.get(id=deal['product_id'])
#         hot_items.append({'title':prod.title,"id":prod.id ,"slug":prod.slug,"selling_price":prod.selling_price,"image":prod.image.name,"sub_cat_tag":prod.subs_category.sub_category_tag})
#     recomended_product = Products_Management.objects.filter(recommended=True).order_by("-created_at")[:8]
#     offers = Offer.objects.all()
#     paginator = Paginator(user_list, 10)
#     product   = Products_Management.objects.all()
#     all_category = Category.objects.all()
#     index = 1
#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         contacts = paginator.page(1)
#     except EmptyPage:
#         contacts = paginator.page(paginator.num_pages)
#     try:
#         form = UserRegistration()
#         if request.method == 'POST':
#             params = request.POST
#             form   = UserRegistration(request.POST or None)
#             if form.is_valid():
#                 obj  = form.save(commit=False)
#                 code = id_generator()
#                 obj.confirmation_code = code
#                 obj.is_active   = False
#                 obj.is_customer = True
#                 obj.is_vendor   = False
#                 ran = random_with_N_digits()
#                 obj.mobile_verification_code = ran
#                 obj.set_password(params['password'])
#                 obj.save()
#                 request.session['email'] = obj.email
#                 messag = "Your JuntosPeru mobile number verification code is : "+str(ran)
#                 temp   = send_sms(obj.mobile,messag)
#                 return render(request, 'resend_otp.html',{"categorys":all_category, "product_list":contacts, 'contacts': contacts})
#             else:
#                 return render(request, 'index.html', {'form': form,"offers":offers,"hot_items":hot_items,"recomended_product":recomended_product,"categorys":all_category, "product_list":contacts, 'contacts': contacts})
#         else:
#             return render(request, 'index.html',{"categorys":all_category, "product_list":contacts, 'contacts': contacts})
#     except Exception as e:
#           print("errorsssssssssssssssssss",e)
#           messages.warning(request, 'Something went wrong !')
#           return redirect("Peru:home")

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


# def subscribe4newsletter(request):
#     if request.method =="POST":
#         email , created = SubscribedEmail.objects.get_or_create(email=request.POST['email'])
#         if created:
#             return HttpResponse(json.dumps({"message":"You have subscribed for news letter", "code":200}), content_type='application/json')
#         else:
#             return HttpResponse(json.dumps({"message":"You have already subscribed for news letter", "code":400}), content_type='application/json')

class SubscribeNewsLetter(View):
	"""docstring for SubscribeNewsLetter"""
	def get(self,request):
		return HttpResponse(json.dumps({"message":"You have subscribed for news letter", "code":200}), content_type='application/json')

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



# def add_to_cart(request):
#     print('dfdfdfdsfdsfdsf--------------------',)
#     try:
#         params = request.POST
#         # a=params['product_id']
#         # b=params['quantity']

#         # print("priiiiiiiiiiiiii",a)
#         # print("priiiiiiiiiiiiii",b)

#         user = request.user
#         exists = None
#         product_obj   = Products_Management.objects.get(id=params['product_id'])
#         price_on_cart = (product_obj.selling_price*int(params['quantity']))
#         print("aaaaaa",price_on_cart)
#         product_card  = Cart.objects.filter(product=product_obj, user=user)
#         if product_card.exists():
#             product_card = product_card.first()
#             product_card.quantity = params['quantity']
#             product_card.product_size = params.get('size',None)
#             product_card.product_color = params.get('color',None)
#             product_card.price = price_on_cart
#             product_card.save()
#             exists = True
#         else:
#             card = Cart(user=request.user, active=True, product=product_obj)
#             card.quantity=params['quantity']
#             card.product_size=params.get('size',None)
#             card.product_color=params.get('color',None)
#             card.price=price_on_cart
#             card.save()
#         cart_count = user.card_user.count()
#         # print("348---cart--3",cart_count)
#         # return render(request, 'index.html', {"cart_count": cart_count, "code":200,'exists':exists})
#         return HttpResponse(json.dumps({"cart_count": cart_count, "code":200,'exists':exists}), content_type='application/json')
#     except Exception as e:
#         # print("dsfhbdshjfdsexceptionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",e)
#         cart_count = request.user.card_user.count()
#         return HttpResponse(json.dumps({"cart_count": cart_count, "code":500}), content_type='application/json')



# @register.filter("truncate_chars")
# def product_detail(request, slug=None):
#     # try:
#     detail = Products_Management.objects.filter(slug=slug).first()
#     product_color = detail.product_colors
#     product_rating = detail.product_reviews.aggregate(Avg('rating_value'))['rating_value__avg']
#     if not product_rating:
#         product_rating = 0
#     total_review = detail.product_reviews.all()
#     # print(total_review)
#     seller = detail.vendor.first_name
#     if product_color.exists():
#         if request.GET.get('color',None):
#             try:
#                 product_images = product_color.get(id=request.GET.get('color')).product_color_images.values()
#             except:
#                 product_images = product_color.last().product_color_images.values()
#         else:
#             product_images = product_color.last().product_color_images.values()
#     else:
#         product_images = None
#     related_products = detail.subs_category.sub_cat_product.filter(selling_price__lte=detail.selling_price).exclude(id=detail.id)[:5]
#     # print(detail.subs_category.sub_category_flage)
#     context =  {'details':detail,
#                 'colors':product_color,
#                 "images":product_images,
#                 "total_review":total_review,
#                 "flage": True if detail.subs_category.sub_category_flage=="CLOTH"  else False ,
#                 "related_products":related_products,
#                 'seller':seller,
#                 'rating_comp':int(product_rating),
#                 'loop_count':range(1,6)}
#     return render(request, 'product.html',context)	
class ProductDetail(View):
	"""docstring for ProductDetail"""
	def get(self,request,slug=None):
		queryset = ProductsManagement.objects.all()
		product = get_object_or_404(queryset,slug=slug)
		relatedProducts = ProductsManagement.objects.filter(subs_category=product.subs_category).exclude(id=product.id)[:5]
		return render(request, 'product.html',{"details":product,"related_products":relatedProducts})	


# def view_cart(request, address=None):
#     user = request.user
#     if user.is_authenticated and user.is_customer:
#         if address:
#             shipa = Shipping_Address.objects.filter(user=user)
#             if shipa.exists():
#                 shipa.update(selected = False)
#                 try:
#                     ship = Shipping_Address.objects.get(id=address)
#                     ship.selected = True
#                     ship.save()
#                 except:
#                     messages.error(request,"No Address selected !")
#         product_cart = Cart.objects.filter(user=user)
#         if product_cart:
#             product_p = product_cart[0].product
#             related_category = product_p.category
#             related_sub_category = product_p.subs_category
#             related_post = Products_Management.objects.filter(category=related_category,subs_category=related_sub_category).exclude(id=product_cart[0].product.id)[:5]
#         else:
#             related_post = []

#         sub_total    = product_cart.aggregate(Sum('price'))['price__sum']
#         if sub_total:
#             grand_total = sub_total
#             total_price = grand_total
#         else:
#             grand_total = 0.0
#             total_price = grand_total
#         if len(product_cart):
#             pro_detail = product_cart[len(product_cart)-1]
#         elif len(product_cart)==0:
#             pro_detail = {}
#         return render(request, 'new_view_cart.html', {"all_cart":pro_detail, "sub_total": sub_total, "grand_total": grand_total,"cart_count":len(product_cart),"total_price":total_price,"related_post":related_post})
#     else:
#         card_Array = []
#         total_price = 0.0
#         if 'card_data' in request.POST and request.POST['card_data']:
#             for items in ast.literal_eval(request.POST['card_data']):
#                 product = Products_Management.objects.get(id=int(items['product_id']))
#                 card_Array.append({
#                         "product":product,
#                         "product_size":int(items['size']),
#                         "product_color": int(items['color']),
#                         "quantity": int(items['quantity']),
#                         "price": product.selling_price * int(items['quantity'])
#                     })
#                 total_price = total_price + product.selling_price * int(items['quantity'])
#             related_post_category = card_Array[-1]['product'].category
#             related_post_sub_category = card_Array[-1]['product'].subs_category
#             related_post = Products_Management.objects.filter(category=related_post_category,subs_category=related_post_sub_category).exclude(id=card_Array[-1]['product'].id)[:5]
#             return render(request, 'new_view_cart.html', {"all_cart":card_Array[-1], "sub_total": 0.0, "grand_total": 0.0,"cart_count":len(card_Array),"total_price":total_price,"related_post":related_post,"product":product})
#         else:
#             return render(request, 'new_view_cart.html', {"all_cart":[], "sub_total": 0.0, "grand_total": 0.0})

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
			total_price = 0.0
			product_cart = Cart.objects.filter(user=user)
			total_price = product_cart.aggregate(Sum('price'))['price__sum']
			total_price = total_price + (total_price * 18)/100
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

class CustomerReview(View):
	"""docstring for CustomerReview"""
	def post(self,request):
		params = request.POST
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
		print("Inside Shipping")
		shipping = ShippingAddress.objects.filter(user=request.user)
		if request.user.is_authenticated() and request.user.is_customer and shipping:
			return redirect("Juntos:customer-order-summary")
		else:
			return render(request, 'shipping_billing.html')


class CustomerOrderSummary(View):
	"""docstring for CustomerOrderSummary"""
	def get(self,request):
		print("Inside Order Summary")
		if request.user.is_customer:
			return render(request, "order-summary.html")
		else:
			messages.info(request, "You are not authorize to access this page.")
			return redirect("Juntos:home")


def order_payment(request):
    user = request.user
    if request.method == 'POST':
        if shipping_address:
            product_cart = Cart.objects.filter(user=user)
            user_data = []
            cart_items = Cart.objects.filter(user=user)
            admin_commission = 0
            for cart in cart_items:
                if not any( vendor.get('email') == cart.product.vendor.email for vendor in user_data):
                    total_pay = cart_items.filter(product__vendor__email=cart.product.vendor.email).aggregate(Sum('price'))['price__sum']
                    chek_price = (total_pay*23)/100
                    total_payment = chek_price + total_pay
                    price = total_payment - total_payment*5/100
                    user_data.append({"email":cart.product.vendor.email, "amount": int(price)})
                else:
                    pass
                admin_commission +=  cart.price*5/100
            respons_url =  payment(user_data, admin_commission, user)
            if respons_url['ack']=="Success":
                return redirect(respons_url['url'])
            else:
                messages.error(request, respons_url['error'][0]['message'])
                return render(request, "payment.html",{"errorId":respons_url['error'][0]['errorId']})
        else:
            messages.error(request, "Please select your order shiping address")
            return redirect("customer:add_shipping")
    else:
        product_cart = Cart.objects.filter(user=user, product__payment_method__case_on_delivery=True)
        return render(request, "payment.html",{"card_product":product_cart})

class OrderPayment(View):
	"""docstring for OrderPayment"""
	def get(self,request):
		return render(request, "payment.html")

def create_order(user, shiping_address):
	cart = Cart.objects.filter(user=user)
	base_price = cart.aggregate(Sum('price'))['price__sum']
	shipping_charge = (base_price*5)/100
	tax_charges = (base_price*18)/100
	total_price = base_price+shipping_charge+tax_charges
	order = CustomerOrder.objects.create(shipping_address=shiping_address,customer=user,order_payment_type='COD',delivery_date=(datetime.today()+timedelta(days=8)).date(),base_price=base_price,shipping_charge=shipping_charge,tax_charges=tax_charges,total=total_price)
	order_items(cart,order)

def order_items(cart,order):
	for obj in cart:
		shipping_charge = (obj.price*5)/100
		tax_charges = (obj.price*18)/100
		total_price = obj.price+shipping_charge+tax_charges
		OrderItems.objects.create(order=order,product=obj.product,product_color=obj.product_color,product_size=obj.product_size,quantity=obj.quantity,base_price=obj.price,shipping_charge=shipping_charge,tax_charges=tax_charges,total=total_price)
		obj.product.product_quantity = obj.product.product_quantity - obj.quantity
		obj.product.save()
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

class CODOrder(View):
	"""docstring for CODOrder"""
	def get(self,request):
		if request.user.is_customer:
			address = ShippingAddress.objects.filter(user=request.user).latest('created_at')
			if address:
				create_order(request.user,address)
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


def recommended(request):
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
        messages.info(request,"no recommended avaialable")
        return redirect("Peru:home")

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


# def advertisement_detail(request, slug=None,tx=None,amt=None):
#     sb_ct= Sub_Category.objects.filter(sub_category_tag="VP")
#     advertisement = Advertisement.objects.get(slug=slug)
#     total_review = advertisement.reviews_adv.all()
#     image_data = Advertisement_Image.objects.filter(advertisement_images=advertisement.id)
#     print("image_data",image_data)
#     related_services = Advertisement.objects.filter(type_of_services=advertisement.type_of_services,location=advertisement.location).exclude(slug=slug)
#     return render(request, 'detail_advertisement.html', {'all_image':image_data,'ads_details':advertisement, 'related_services':related_services, 'total_review':total_review, 'res_cat':sb_ct})


class AdvertisementDetail(View):
	"""docstring for AdvertisementDetail"""
	def get(self,request,slug=None,tx=None,amt=None):
		sb_ct= SubCategory.objects.filter(sub_category_tag="VP")
		advertisement = Advertisement.objects.get(slug=slug)
		# total_review = advertisement.reviews_adv.all()
		related_services = Advertisement.objects.filter(type_of_services=advertisement.type_of_services,location=advertisement.location).exclude(slug=slug)
		return render(request, 'detail_advertisement.html', {'ads_details':advertisement, 'related_services':related_services,'res_cat':sb_ct})

		
# @login_required(login_url="/")
# def advertisments_review(request):
#     params = request.POST
#     slug = params['slug']
#     adv = Advertisement.objects.get(id=params['advertisement_reviews'])
#     review = Advertisment_Review.objects.create(advertisement_reviews=adv,
#                                              content=params['content'],
#                                              rating_value=params['rating_value'],
#                                              given_by=request.user)
    
#     return redirect("customer:ad_detail", slug)

class AdvertismentsReview(View):
	"""docstring for AdvertismentsReview"""
	def get(self,request):
		params = request.POST
		slug = params['slug']
		adv = Advertisement.objects.get(id=params['advertisement_reviews'])
		review = Advertisment_Review.objects.create(advertisement_reviews=adv,content=params['content'],rating_value=params['rating_value'],given_by=request.user)
		return redirect("Juntos:advertisment-detail", slug)

	
				
	
						
														