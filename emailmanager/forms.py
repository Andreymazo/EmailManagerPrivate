from django import forms
from config import settings
# host_choices = ((1,settings.EMAIL_HOST), (2,settings.SECOND_EMAIL_HOST))

class HostChoice_1(forms.Form):
    host_1 = forms.CharField()#choices=host_choices)
    email_1 = forms.CharField()
    password_1 = forms.CharField()

class HostChoice_2(forms.Form):
    host_2 = forms.CharField()
    email_2 = forms.CharField() 
    password_2 = forms.CharField()
