from django.urls import path

from payment.views import RentPaymentView, PaymentCreateView

urlpatterns = [
    path('payment', RentPaymentView.as_view(), name='payment_list'),
    path('payment/<int:house_id>/<int:year>/<int:month>', PaymentCreateView.as_view(), name='payment_create'),
]