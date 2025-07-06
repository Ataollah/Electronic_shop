import re
import smtplib
import string
from datetime import timedelta
from email.mime.text import MIMEText
from random import choice
import requests
from django.utils import timezone
from appuser.models import VerificationUser
from siteInfo.models import SMSProvider, MailProvider, SiteInfo


def generate_verification_code():
    chars = string.digits
    random_str = ''.join(choice(chars) for _ in range(4))
    return random_str


class SmsSender:
    def __init__(self):
        self.sms_provider = SMSProvider.objects.all().first()

    def send_sms(self,to, message):
        url = self.sms_provider.api_url + 'SendBatchSms'
        data = {'userName': self.sms_provider.username,
                'password': self.sms_provider.password,
                'fromNumber': self.sms_provider.phone_number,
                'toNumbers': to,
                'messageContent': message,
                'isFlash': False,
                'sendDelay': 0
                }
        print('message send to ', to)
        print('message is : ', message)
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(response.text)

class EmailSender:

    def __init__(self):
        self.mail_provider = MailProvider.objects.all().first()

    def send_email(self, subject, body, recipients):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.mail_provider.smtp_sender_email
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.mail_provider.smtp_sender_email, self.mail_provider.smtp_sender_password)
            smtp_server.sendmail(self.mail_provider.smtp_sender_email, recipients, msg.as_string())
        print("Message sent!")

class VerificationMessageSender:
    def __init__(self, username):
        self.username = username
        self.website_name = SiteInfo.objects.all().first().name

    def _check_username(self):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        phone_pattern = r'^09[0-9]{9}$'

        if re.match(email_pattern, self.username):
            return 'email'
        elif re.match(phone_pattern, self.username):
            return 'phone'
        else:
            return 'invalid'


    def _save_verification_code(self, verification_code):
        now_plus_5m = timezone.now() + timedelta(minutes=5)

        candidate_user = VerificationUser.objects.filter(username=self.username).first()

        if candidate_user is not None:
            candidate_user.verification_code = verification_code
            candidate_user.valid_until = now_plus_5m
            candidate_user.save()
        else:
            VerificationUser.objects.create(username=self.username, verification_code=verification_code,
                                         valid_until=now_plus_5m)

    def sendCode(self):
        code = generate_verification_code()
        print('code is ', code)
        self._save_verification_code(code)
        message = f'به {self.website_name} خوش آمدید کد تایید شما {code} باتشکر'
        if self._check_username() == 'email':
            sender = EmailSender()
            subject = self.website_name + ' کد فعالسازی'
            sender.send_email(subject, message, [self.username])
        elif self._check_username() == 'phone':
            sender = SmsSender()
            #sender.send_sms(self.username, message)
        else:
            print("Invalid Username")
            

