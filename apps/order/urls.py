from django.urls import path
from .views import TestView
# from apps.order.views import GeneratePayLinkAPIView


urlpatterns = [
    path('payme/endpoint/', TestView.as_view(),),
    # path('pay-link/', GeneratePayLinkAPIView.as_view(), name='generate-pay-link')
]