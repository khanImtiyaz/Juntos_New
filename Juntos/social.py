from slugify import slugify

def social(backend, user, response, *args, **kwargs):
	print(kwargs['details'])
	user.first_name = kwargs['details']['first_name']
	user.last_name = kwargs['details']['last_name']
	user.slug = slugify(kwargs['details']['first_name']+kwargs['details']['last_name'])
	user.otp_creation()
	user.mobile_verified = True
	user.is_customer = True
	user.is_vendor = user.is_vendor
	user.login_type = "facebook"
	user.confirmation_code = "Confirmed"
	user.save()
