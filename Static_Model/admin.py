from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

# Register your models here.


class FAQsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(attrs={'rows':10, 'cols':100}))
    class Meta:
        model = JuntosFAQs
        fields = ["faq_matter","content"]
@admin.register(JuntosFAQs)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ["faq_matter","content"]
    form = FAQsForm

class AboutUsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(attrs={'rows':10, 'cols':100}))
    class Meta:
        model = JuntosAboutus
        fields = ["header","content"]
@admin.register(JuntosAboutus)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ["header","content"]
    form = AboutUsForm

class CareersForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(attrs={'rows':10, 'cols':100}))
    class Meta:
        model = JuntosCareers
        fields = ["heading","content"]
@admin.register(JuntosCareers)
class CareersAdmin(admin.ModelAdmin):
    list_display = ["heading","content"]
    form = CareersForm
    
class TermConditionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(attrs={'rows':10, 'cols':100}))
    class Meta:
        model = JuntosTermCondition
        fields = ["heading","content"]
@admin.register(JuntosTermCondition)
class TermModelAdmin(admin.ModelAdmin):
    list_display = ["heading","content","created_at"]
    form = TermConditionForm


class ContactUsForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorWidget(attrs={'rows':10, 'cols':100}))
    class Meta:
        model = JuntosContactUs
        fields = ["contact_user", "message"]
        
@admin.register(JuntosContactUs)
class JuntosContactUsAdmin(admin.ModelAdmin):
    list_display = ["message","contact_user"]
    form = ContactUsForm

class JuntosContactEmailAdmin(admin.ModelAdmin):
    list_display = ["contactemail","subject","message"]
admin.site.register(JuntosContactEmail,JuntosContactEmailAdmin)

admin.site.register(SubscribeNewsLetter)


