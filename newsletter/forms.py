from django import forms

from newsletter.models import Subscriber


class SubscriberForm(forms.ModelForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('ایمیل نمی‌تواند خالی باشد.')
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError('ایمیل معتبر نیست.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت‌نام شده است.')

        return cleaned_data

    class Meta:
        model = Subscriber
        fields = ['email']

