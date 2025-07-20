import requests
from siteInfo.models import SMSProvider

class SmsSender:
    def __init__(self):
        self.sms_provider = SMSProvider.objects.first()

    def send_sms(self, to, message):
        if not self.sms_provider:
            print("SMS Provider is not configured.")
            print(f"Message: {message}\nTo: {to}\nMessage not sent.")
            return

        url = f"{self.sms_provider.api_url}SendBatchSms"
        data = {
            'userName': self.sms_provider.username,
            'password': self.sms_provider.password,
            'fromNumber': self.sms_provider.phone_number,
            'toNumbers': to,
            'messageContent': message,
            'isFlash': False,
            'sendDelay': 0
        }

        print(f"Message sent to: {to}\nMessage: {message}")
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        print(response.text)