from siteInfo.models import SiteInfo, MailProvider
from email.mime.text import MIMEText
import smtplib


class EmailSender:
    def __init__(self):
        self.mail_provider = MailProvider.objects.first()

    def send_email(self, subject, body, recipients):
        if not self.mail_provider:
            print("Mail provider is not configured.")
            return

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.mail_provider.smtp_sender_email
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.mail_provider.smtp_sender_email, self.mail_provider.smtp_sender_password)
            smtp.sendmail(msg['From'], recipients, msg.as_string())
        print("Email sent successfully!")
