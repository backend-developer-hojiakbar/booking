from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from django.urls import path
from apps.blog.models import Booking


class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        print(amount, account)
        order = Booking.objects.filter(id=account["order_id"], pending_status="P").first()
        if not order:
            return self.ORDER_NOT_FOND
        if order.total_sum * 100 != amount:
            return self.INVALID_AMOUNT
        return self.ORDER_FOUND


def successfully_payment(self, account, transaction, *args, **kwargs):
    order = Booking.objects.filter(id=transaction.order_key).first()
    if not order:
        return self.ORDER_NOT_FOND
    order.pending_status = "C"
    order.save()
    print(account)


def cancel_payment(self, account, transaction, *args, **kwargs):
    print(account)


class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


urlpatterns = [
    path('paycom/', TestView.as_view())
]