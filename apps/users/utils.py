from apps.users.models import PhoneToken
import random
import string
from django.utils import timezone
from core.sms import eskiz
from django.core.mail import EmailMessage
from django.conf import settings


def generate_token(phone_number):
    if PhoneToken.objects.filter(phone_number=phone_number).exists():
        phone_token = PhoneToken.objects.filter(phone_number=phone_number).last()
        phone_token.delete()
    phone_token = PhoneToken.objects.create(phone_number=phone_number)
    token = "".join(random.choices(string.digits, k=6))
    phone_token.token = token
    phone_token.expires_at = timezone.now() + timezone.timedelta(minutes=3)
    phone_token.save()
    message = "Thebron sistemasi uchun tasdiqlash kodi: {}".format(token)
    eskiz.send_sms(str(phone_number)[1:], message, from_whom="4546")
    return token


def verify_token(phone_number, token):
    try:
        phone_token = PhoneToken.objects.filter(phone_number=phone_number).last()
        print(phone_token)
        if phone_token.token == token and phone_token.expires_at > timezone.now():
            phone_token.is_verified = True
            phone_token.save()
            print(phone_token)
            return True
        return False
    except PhoneToken.DoesNotExist:
        return False


def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()