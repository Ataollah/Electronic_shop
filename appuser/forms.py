import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from appuser.models import VerificationUser, AppUser
from django.utils import timezone


def enforce_password_policy(password):
    if len(password) < 4:
        raise ValidationError('کلمه عبور باید حداقل 4 کاراکتر باشد')


class CandidPhoneVerificationForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=50)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.match(r'^09\d{9}$', username):
            raise ValidationError('شماره تلفن باید با 09 شروع شود و 11 رقم باشد')
        user = AppUser.objects.filter(username=username).first()
        if user:
            raise ValidationError('نام کاربری تکراری است', code='invalid')
        return username


class UserPhoneVerificationForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=50)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.match(r'^09\d{9}$', username):
            raise ValidationError('شماره تلفن باید با 09 شروع شود و 11 رقم باشد')
        user = AppUser.objects.filter(username=username).first()
        if not user:
            raise ValidationError('نام کاربری موجود نیست ', code='invalid')
        return username


class VerifyCodeForm(forms.Form):
    verification_code = forms.CharField(label='کد تایید', max_length=50)

    def __init__(self, *args, username=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code')
        if verification_code and not re.match(r'^\d{4}$', verification_code):
            raise ValidationError('کد تایید باید 4 رقم باشد')

        candidate = VerificationUser.objects.filter(username=self.username).first()
        if not candidate:
            raise ValidationError('نام کاربری یافت نشد')
        until_valid = candidate.valid_until
        if candidate.verification_code != verification_code:
            raise ValidationError('کد ارسالی اشتباه می باشد')
        if timezone.now() > until_valid:
            raise ValidationError('کد ارسالی منقضی شده است')

        return verification_code


class VerificationUserForm(forms.ModelForm):
    class Meta:
        model = VerificationUser
        fields = ['username', 'verification_code']


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='کلمه عبور جدید', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='تکرار کلمه عبور جدید', widget=forms.PasswordInput)

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        enforce_password_policy(password1)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise ValidationError('کلمه عبور جدید و تکرار آن باید یکسان باشند')
        return password2


class ChangePasswordForm(PasswordChangeForm):

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        enforce_password_policy(password1)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise ValidationError('کلمه عبور جدید و تکرار آن باید یکسان باشند')
        return password2


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(label='نام کاربری', max_length=50)  # Explicitly define the field
    password1 = forms.CharField(label='کلمه عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار کلمه عبور', widget=forms.PasswordInput)
    email = forms.EmailField(label='ایمیل', max_length=50)
    postal_code = forms.CharField(label='کدپستی', widget=forms.TextInput, max_length=10, min_length=10)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = initial.get('username', '')  # Set initial value
        print(self.fields['username'].initial)  # Debugging

    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name','profile_picture', 'email','postal_code'
            ,'province','county','city','district','rural','address']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('نام کاربری نمی‌تواند خالی باشد')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('کلمه عبور و تکرار آن باید یکسان باشند')
        return password2

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isdigit() or len(postal_code) != 10:
            raise ValidationError('کدپستی باید دقیقا ۱۰ رقم باشد')
        return postal_code

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 102400:  # 100 KB = 102400 bytes
                raise ValidationError('حجم تصویر پروفایل نباید بیشتر از ۱۰۰ کیلوبایت باشد')
        return profile_picture

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise ValidationError('ایمیل وارد شده معتبر نیست')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        print('password : ', self.cleaned_data['password1'])  # Debugging
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        print('hashed password : ', user.password)
        # Use names from hidden fields if present
        user.province = self.data.get('province', user.province)
        user.county = self.data.get('county', user.county)
        user.city = self.data.get('city', user.city)
        user.district = self.data.get('district', user.district)
        user.rural = self.data.get('rural', user.rural)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='شماره موبایل', max_length=50)  # Explicitly define the field
    first_name = forms.CharField(label='نام', max_length=50)
    last_name = forms.CharField(label='نام خانوادگی', max_length=50)
    address = forms.CharField(label='آدرس', max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = initial.get('username', '')  # Set initial value
        self.fields['first_name'].initial = initial.get('first_name', '')
        self.fields['last_name'].initial = initial.get('last_name', '')
        self.fields['address'].initial = initial.get('address', '')
        print('first name : ', self.fields['first_name'].initial)  # Debugging

    class Meta:
        model = AppUser
        fields = [
            'username', 'first_name', 'last_name', 'profile_picture', 'email',
            'province', 'county', 'city', 'district', 'rural', 'address', 'postal_code'
        ]


class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'username']
