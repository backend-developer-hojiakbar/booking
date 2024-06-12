from django.urls import path
from apps.crm.views import UserSalesView


urlpatterns = [
    path('userSales/<int:user_id>/', UserSalesView.as_view(), name='userSales'),
]