def social(backend, user, response, *args, **kwargs):
	user.is_customer = True
	user.is_vendor = user.is_vendor
	user.mobile_verified = True
	user.first_name = kwargs['details']['first_name']
	user.login_type = "facebook"
	user.save()
