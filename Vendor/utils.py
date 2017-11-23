from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, timedelta
from Vendor.models import *
import logging
import dhl_shipping
from dhl_shipping import shipment
import os
logging.basicConfig(level=logging.INFO) 


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def dhl_service(order_details, vendor_dhl, invoice):
	vendor_account_info = Vendor_Account_Details.objects.get(vendor=vendor_dhl)
	dhl_shipping.dhl_site_id = 'Juntos'
	dhl_shipping.dhl_site_password = 'w6jDMkWsZI'
	dhl_shipping.dhl_account_no = '803921577'
	address_details = {
	    'from_company_name': vendor_account_info.business_name,
	    'from_address_line_one': vendor_account_info.address1,
	    'from_address_line_two': '',  # optional
	    'from_city': vendor_dhl.city,
	    'from_zipcode': vendor_dhl.pincode,
	    'from_country': 'US',  # two letter abbriviation
	    'from_country_name': vendor_dhl.country,  # country full name
	    'from_name': vendor_dhl.first_name,
	    'from_phone_no': vendor_dhl.mobile,
	    'from_state': vendor_dhl.state,  # only for pickup (from_state) - max 35v char - Optional
	    'from_region_code':'',
	    'from_location_type':'C',
	    'from_package_location':'V',
	    
	    'to_company_name': 'Mobiloitte',
		'to_address_line_one': order_details.order.shipping_address.shipping_address,
		'to_address_line_two': order_details.order.shipping_address.shipping_address,  # optional
		'to_city': order_details.order.shipping_address.shipping_city,
		'to_zipcode': order_details.order.shipping_address.shipping_zip,
		'to_country': order_details.order.shipping_address.shipping_country_abbreviation,  # two letter abbriviation
		'to_country_name': order_details.order.shipping_address.shipping_country,  # country full name
		'to_name': order_details.order.shipping_address.shipping_first_name,
		'to_phone_no': order_details.order.shipping_address.user.mobile,
	}
	pieces_details = []
	for i in range(order_details.quantity):
		piece = {
		    'piece_id': i,
		    'package_type': 'DF',  # DF|YP etc - this one can be made optional as package details has the same param
		    'piece_height': int(order_details.product.product_height),
		    'piece_depth': int(order_details.product.product_depth),
		    'piece_width': int(order_details.product.product_width),
		    'piece_weight':int(order_details.product.product_weight)
		}
		pieces_details.append(piece)

	total_weight = 0 
	for piece in pieces_details:
		total_weight = total_weight + int(piece['piece_weight'])
	package_details = {
		'package_type': 'DF',  # DF|YP etc
		'total_weight': total_weight,  # total weight
		'dimension_unit': 'C',
		'weight_unit': 'K',
		'global_product_code': 'P',
		'local_product_code': 'P',
		'door_to': 'DD',
		'shipment_date': invoice.shippment_date,  # YYYY-mm-dd format
		'content_description': 'Some Content',
		'declared_value': '1.00',
		'declared_currency': 'USD',
		'is_dutiable': 'Y',
		'insured_amount': float(order_details.product.insured_amount),  # Insured Amount (Required if Special Service of I
		'special_service_type': 'I',  # optional
		'reference_id': '1213122'  # any arbitrary or random number
	}
	optional_data = {
	    'awb_pdf_file_path': os.path.expanduser('~/Desktop'),
	    'awb_pdf_file_name': '{}.pdf'.format(order_details.id),  # name of the file
	     "return_pdf_file" : True
	}
	pickup_details = {
		'pickup_date': invoice.pickup_date,  # YYYY-MM-DD format
		'ready_by_time': invoice.ready_by_time,  # hh:mm ie 14:35
		'close_time': invoice.close_time,  # hh:mm ie 15:35
	}

	shipment_data_to_send = { 
	'addresses':address_details, 
	'package': package_details, 
	'pieces': pieces_details, 
	'pickup_details':pickup_details, 
	'optional_data': optional_data
	}
	dict_response = shipment.get_shipment(shipment_data_to_send)
	print(dict_response)
