from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from dateutil.parser import parse
import sys
import traceback
import logging
import time
from Log.models import LogTracker
from Juntos.urls import urlpatterns as Jurlpatterns
from Vendor.urls import urlpatterns as Vurlpatterns


LIST_APP_FOR_LOGGING = ['Juntos','Vendor']


class LoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.start_time = time.time()
        self.request_body = request.POST
        self.request_get_params = request.GET

    def process_response(self,request,response):
        try:
            logInstance = LogTracker()
            logInstance.remote_address = request.META.get('REMOTE_ADDR')
            logInstance.request_user = request.user
            logInstance.method_type = request.method
            logInstance.method_name = request.get_full_path()
            if self.request_body:
                logInstance.request_length = sys.getsizeof(self.request_body)/float(1000)
                logInstance.request_content = self.request_body
            logInstance.response_status_type = response.status_code
            if response.content:
                logInstance.response_length = sys.getsizeof(response.content)/float(1000)
                logInstance.response_content = response.content

            print("Reverse",request.resolver_match.namespace)
            if request.get_full_path() in LIST_APP_FOR_LOGGING:
                print("Body",self.request_body)
                print("Response Status",response.status_code)


        except Exception as e:
            print("Exception as e",e)
        return response

