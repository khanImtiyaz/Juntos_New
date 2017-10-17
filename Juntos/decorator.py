from functools import wraps
from .models import *


def has_cart(view_func):
	def _decorator(request, *args, **kwargs):
		print("Inside",request)
		cartObj = Cart.objects.filter(user=request.user)
		if cartObj:
			response = view_func(request, *args, **kwargs)
			return response
		else:
			return None
	return wraps(view_func)(_decorator)