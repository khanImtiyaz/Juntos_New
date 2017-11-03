from django.db import models
from django.template.defaultfilters import truncatechars


# Create your models here.
class LogTracker(models.Model):
    remote_address = models.CharField(("IP URL"),null=True, blank=True, max_length=255)
    user_email = models.CharField(("Request User"),null=True, blank=True, max_length=255)
    method_type = models.CharField(("Method Type"),null=True, blank=True, max_length=255)
    method_name = models.CharField(("API Name"),null=True, blank=True, max_length=255)
    request_content = models.TextField(("Request Parameter"),null=True, blank=True)
    request_length = models.CharField(("Request Size in KB"), null=True, blank=True, max_length=255)
    response_status_type = models.CharField(("Response Status"),null=True, blank=True, max_length=255)
    response_content = models.TextField(("Response Content"),null=True, blank=True)
    response_length = models.CharField(("Response Size in KB"),null=True, blank=True, max_length=255)
    time_taken = models.FloatField(("Response Time"),null=True, blank=True)
    extra_log = models.TextField(("Extra Log"),null=True, blank=True)
    exception_full_stack_trace = models.TextField(null=True, blank=True)
    exception_short_value = models.CharField(null=True, blank=True, max_length=255)
    request_datetime = models.DateTimeField(auto_now=True)

    @property
    def short_request_content(self):
        return truncatechars(self.request_content, 100)

    @property
    def short_response_content(self):
        return truncatechars(self.response_content, 100)

    @property
    def short_exception_full_stack_trace(self):
        return truncatechars(self.exception_full_stack_trace, 100)
