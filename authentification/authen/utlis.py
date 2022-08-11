from unittest.util import safe_repr
from django.core.mail import EmailMessage
class util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['email_to']])
        email.send()
