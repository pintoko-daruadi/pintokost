from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('landlord/new', views.LandlordSignupView.as_view(), name='landlord_new'),
    path('renter/new', views.ProfileCreateView.as_view(), name='renter_new'),
]
