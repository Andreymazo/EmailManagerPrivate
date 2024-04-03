from django import forms
from config import settings

class HostChoice(forms.Form):
    host_choices = [settings.EMAIL_HOST, settings.SECOND_EMAIL_HOST]
    host = forms.ChoiceField(choices=host_choices)

    host_1 = forms.CharField()
    host_2 = forms.CharField()

    hosts = []