from django import forms

from siteInfo.models import ContactUS


class ContactUSForm(forms.ModelForm):
    class Meta:
        model = ContactUS
        fields = '__all__'



