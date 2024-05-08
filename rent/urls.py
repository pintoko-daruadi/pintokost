from django.urls import path

from rent.views import PaymentCreateView, RentCreateView, RentDeleteView, RentPaymentView


app_name = 'rent'

urlpatterns = [
    path('payment', RentPaymentView.as_view(), name='list'),
    path('payment/<int:house_id>/<int:year>/<int:month>', PaymentCreateView.as_view(), name='create'),
    path('<int:house_id>', RentCreateView.as_view(), name='rent_create'),
    path('<int:house_id>/deactivate', RentDeleteView.as_view(), name='rent_deactivate'),
]