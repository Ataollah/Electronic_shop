from django import forms
from appuser.models import AppUser


class ExtraOrderInfoForm(forms.Form):
    description = forms.CharField(label='Description', max_length=100, required=False)


class OrderAddressForm(forms.Form):
    province = forms.CharField(label='Province', max_length=100,required=True)
    county = forms.CharField(label='Province', max_length=100, required=True)
    district = forms.CharField(label='Province', max_length=100, required=True)
    city = forms.CharField(label='Province', max_length=100, required=True)
    rural = forms.CharField(label='Province', max_length=100, required=False)
    address = forms.CharField(label='Province', max_length=100, required=True)
    postal_code = forms.CharField(label='Province', max_length=100, required=True)
