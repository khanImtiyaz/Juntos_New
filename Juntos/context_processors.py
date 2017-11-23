from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta
import datetime
from Static_Model.models import *
from .models import *

def taxValue(value):
    return {"tax":TaxPercentage.objects.first()}

def newsSection(value):
    return {"news":News.objects.all()}

def categoriesData(request):
    category = Category.objects.all().order_by('priority')
    return {"categories":category}

def about(request):
    content = JuntosAboutus.objects.first()
    return {"abouts":content}
    
def starRating(request):
    return {"star_rating":[1,2,3,4,5]}

def cart(request):
	if request.user.is_authenticated() and request.user.is_customer:
		delivery_date = (datetime.today()+timedelta(days=8)).date()
		cartObj = Cart.objects.filter(user=request.user)
		tax = TaxPercentage.objects.first()
		if cartObj:
			has_COD = cartObj.filter(product__payment_mode__contains=['COD'])
			cart_sum = cartObj.aggregate(Sum('price'))
			total_amount = float(cart_sum['price__sum'])+  float((cart_sum['price__sum']*int(tax.tax))/100)
			# shipping_amount = total_amount + ((total_amount*5)/100)
			shipping_amount = total_amount
			
			return {"total_amount":total_amount,"shipping_amount":shipping_amount,"cart_obj":cartObj,"delivery_date":delivery_date,"has_COD":True if len(cartObj) is len(has_COD) else False}
		return {"total_amount":"","shipping_amount":"","cart_obj":cartObj,"delivery_date":"","has_COD":""}
	else:
		return {"total_amount":{},"shipping_amount":{},"cart_obj":{},"delivery_date":{},"has_COD":{}}

def userShippingDetail(request):
	if request.user.is_authenticated() and request.user.is_customer:
		address = ShippingAddress.objects.filter(user=request.user)
		if address:
			address = address.latest('created_at')
			return {"address":address}
		else:
			return {"address":{}}
	else:
		return {"address":{}}
	
def unreadCount(request):
	if request.user.is_authenticated() and request.user.is_vendor:
		count = Notifications.objects.filter(vendor=request.user,is_read=False)
		return  {"notification_unread_count":count}
	return {"notification_unread_count":[]}


def bannerList(request):
	banner = Banner.objects.all()
	return {"banner_list": banner}