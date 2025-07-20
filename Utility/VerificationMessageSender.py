import re
from datetime import timedelta
from django.utils import timezone
from appuser.models import VerificationUser
from siteInfo.models import SiteInfo
from Utility.EmailSender import EmailSender
from Utility.SmsSender import SmsSender
import string
from random import choice


class VerificationMessageSender:
    def __init__(self, username):
        self.username = username
        self.website_name = SiteInfo.objects.first().name or 'وبسایت شما'

    def _check_username(self):
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.username):
            return 'email'
        if re.match(r'^09[0-9]{9}$', self.username):
            return 'phone'
        return 'invalid'

    def _save_verification_code(self, code):
        valid_until = timezone.now() + timedelta(minutes=5)
        user = VerificationUser.objects.filter(username=self.username).first()
        if user:
            user.verification_code = code
            user.valid_until = valid_until
            user.save()
        else:
            VerificationUser.objects.create(username=self.username, verification_code=code, valid_until=valid_until)

    def sendCode(self):
        code = ''.join(choice(string.digits) for _ in range(4))
        self._save_verification_code(code)
        message = f'به {self.website_name} خوش آمدید کد تایید شما {code} باتشکر'
        if self._check_username() == 'email':
            EmailSender().send_email(f'{self.website_name} کد فعالسازی', message, [self.username])
        elif self._check_username() == 'phone':
            SmsSender().send_sms(self.username, message)
        else:
            print("Invalid Username")