from django import template
from django.utils.translation import pgettext, ugettext as _, ungettext
from django.utils.timezone import is_aware, utc, get_current_timezone
from django.template import defaultfilters
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


# @register.filter
# def thriceArray(value):
#     result = [value[i:i+3] for i in xrange(0, len(value), 3)]
#     return result[1:]


# @register.filter
# def is_digit(value):
#     # result = value.isdigit() 
#     result =  isinstance(value,int) or isinstance(value,float) or value.isdigit()
#     return result

# @register.filter
# def natural_time(value):
#     """
#     Returns a 'natural' representation of the given time.
#     Formats similar to Facebook.
#     Based on django.contrib.humanize.naturaltime

#     If given time occurred today, prints 'x seconds/minutes/hours ago'
#     If given time occurred yesterday, prints 'yesterday at xx:xx'
#     If given time occurred more than 1 day ago, prints full date
#     """
#     if not isinstance(value, date):  # datetime is a subclass of date
#         return value

#     current_timezone = get_current_timezone()
#     now = datetime.now(current_timezone)
#     yesterday = now - timedelta(days=1)
#     value = value.astimezone(current_timezone) # localize timezone

#     delta = now - value
#     if value.date() == yesterday.date():
#         return _('yesterday at %(time)s') % {'time': defaultfilters.time(value, 'TIME_FORMAT')}
#     elif delta.days != 0:
#         return defaultfilters.date(value, 'DATETIME_FORMAT')
#     elif delta.seconds == 0:
#         return _('now')
#     elif delta.seconds < 60:
#         return ungettext(
#             # Translators: please keep a non-breaking space (U+00A0)
#             # between count and time unit.
#             'a second ago', '%(count)s seconds ago', delta.seconds
#         ) % {'count': delta.seconds}
#     elif delta.seconds // 60 < 60:
#         count = delta.seconds // 60
#         return ungettext(
#             # Translators: please keep a non-breaking space (U+00A0)
#             # between count and time unit.
#             'a minute ago', '%(count)s minutes ago', count
#         ) % {'count': count}
#     else:
#         count = delta.seconds // 60 // 60
#         return ungettext(
#             # Translators: please keep a non-breaking space (U+00A0)
#             # between count and time unit.
#             'an hour ago', '%(count)s hours ago', count
#         ) % {'count': count}



