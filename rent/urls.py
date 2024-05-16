from django.urls import path

from rent.views import RentCreateView, RentDeleteView


app_name = 'rent'

urlpatterns = [
    path('<int:house_id>', RentCreateView.as_view(), name='create'),
    path('<int:house_id>/deactivate', RentDeleteView.as_view(), name='deactivate'),
]