from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta
import datetime
from Static_Model.models import *
from .models import *



def categories_data(request):
    category = Category.objects.all().order_by('priority')
    return {"categories":category}

def about(request):
    content = JuntosAboutus.objects.first()
    return {"abouts":content}

def products(request):
    product = ProductsManagement.objects.all().exclude(expire_products=0)
    return {"all_product_list":product}

def star_rating(request):
    return {"star_rating":[1,2,3,4,5]}

def cart(request):
	if request.user.is_authenticated():
		delivery_date = (datetime.today()+timedelta(days=8)).date()
		cartObj = Cart.objects.filter(user=request.user)
		if cartObj:
			has_COD = cartObj.filter(product__payment_mode__contains=['COD'])
			cart_sum = cartObj.aggregate(Sum('price'))
			total_amount = float(cart_sum['price__sum'])+  float((cart_sum['price__sum']*18)/100)
			shipping_amount = total_amount + ((total_amount*5)/100)
			return {"total_amount":total_amount,"shipping_amount":shipping_amount,"cart_obj":cartObj,"delivery_date":delivery_date,"has_COD":True if len(cartObj) is len(has_COD) else False}
		return {"total_amount":"","shipping_amount":"","cart_obj":cartObj,"delivery_date":"","has_COD":""}
	else:
		return {"total_amount":"","shipping_amount":"","cart_obj":"","delivery_date":"","has_COD":""}

def userShippingDetail(request):
	if request.user.is_authenticated():
		address = ShippingAddress.objects.filter(user=request.user).latest('created_at')
		return {"address":address}
	else:
		return {"address":""}
	


# def all_data(request):
# 	banner = Banner.objects.all()
# 	return {"banner_list": banner}


# def all_category_data(request):
# 	all_category=Category.objects.all()
# 	return {"categorys": all_category}


# def all_offer_data(request):
# 	offers = Offer.objects.all()
# 	return {"offers": offers}


# def all_hot_item(request):
# 	hot_items = []
# 	hot_deals = CustomerOrder_items.objects.values("product_id").annotate(Count("product_id")).order_by("-product_id__count")[:5]
# 	for deal in hot_deals:
# 		prod = Products_Management.objects.get(id=deal['product_id'])
# 		hot_items.append({'title': prod.title, "id": prod.id, "slug": prod.slug, "selling_price": prod.selling_price, "image": prod.image.name, "sub_cat_tag": prod.subs_category.sub_category_tag})
# 	return {"hot_items": hot_items}