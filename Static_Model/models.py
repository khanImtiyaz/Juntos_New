from django.db import models
from Juntos.models import MyUser


####   Static Content




class JuntosTermCondition(models.Model):
    heading = models.CharField('Heading', max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Juntos Terms and Conditions"
       
       
class JuntosCareers(models.Model):
    heading = models.CharField('Heading', max_length=100, null=True, blank=True)
    content = models.TextField('Message', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Juntos Careers"


class JuntosContactUs(models.Model):
    message = models.TextField(null=True, blank=True)
    contact_user = models.ForeignKey(MyUser, related_name='contact_user')
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "List of Contacted Customer"


# class JuntosContactUsEmail(models.Model):
#     contactemail = models.EmailField(('Email Address'), max_length=50,null=True)
#     subject = models.CharField("Subject",max_length=100,blank=True,null=True)
#     message = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Contact Details"


class JuntosFAQs(models.Model):
    faq_matter = models.CharField('FAQs subject', max_length=200, blank=False)
    content = models.TextField(null=True, blank=True)
    asked_user = models.ForeignKey(MyUser, related_name='asked_user', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.faq_matter
    
    class Meta:
        verbose_name_plural = "List of FAQs"


class JuntosAboutus(models.Model):
    header = models.CharField('About subject', max_length=200, blank=False)
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About us"


class SubscribeNewsLetter(models.Model):
    email = models.EmailField(('Email Address'), max_length=50,unique=True)
    class Meta:
        verbose_name_plural = "Subscribe News Letter"
