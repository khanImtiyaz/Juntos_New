from django import template
from django.utils.translation import pgettext, ugettext as _, ungettext
from django.utils.timezone import is_aware, utc, get_current_timezone
from django.template import defaultfilters
from django.db.models import Avg
from datetime import date, datetime, timedelta
from Juntos.models import *

register = template.Library()


@register.filter
def adv(value):
    # return News.objects.all()
    return {}

@register.filter
def product_quantity(value):
	result = []
	for i in range(1,value+1):
		result.append(i)
	return result

@register.filter
def tax(value,quantity):
	return quantity*(value + ((value*18)/100))


@register.filter
def thriceArray(value):
    result = [value[i:i+3] for i in range(0, len(value), 3)]
    return result[1:]

@register.filter
def percentageValue(sell,actual):
    return int(((actual-sell)*100)/actual)

@register.filter
def convertToList(value):

	return value.split(",")
	
@register.filter
def colorCode(value):
	color = ProductColor.objects.get(id=value)
	return color.color

@register.filter
def buyornot(value,user):
	for obj in value:
		if obj.order.customer==user:
			return True
	return False

@register.filter
def productRating(value):
	review = CustomerReview.objects.filter(product=value).aggregate(Avg('rating'))
	return review['rating__avg']

@register.filter
def ratingCount(value):
	count = CustomerReview.objects.filter(product=value).count()
	print("----------count---------",count)
	return count



