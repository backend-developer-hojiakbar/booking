from eskiz_sms import EskizSMS
from django.conf import settings


ESKIZ_EMAIL=settings.ESKIZ_EMAIL
ESKIZ_PASSWORD=settings.ESKIZ_PASSWORD

eskiz = EskizSMS(
            email=ESKIZ_EMAIL,
            password=ESKIZ_PASSWORD,
        )
# eskiz.send_sms(str(number)[1:], message, from_whom='4546')
