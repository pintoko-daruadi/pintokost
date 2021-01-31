from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('landlord/signup', views.LandlordSignupView.as_view(), name='landlord_signup'),
    path('renter/add', views.ProfileCreateView.as_view(), name='add'),
]
