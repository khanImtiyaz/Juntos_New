from django.db.models import Sum, Avg, Count
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