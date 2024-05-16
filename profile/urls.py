from django.urls import path

from profile.views import LandlordSignupView, ProfileCreateView

app_name = 'profile'

urlpatterns = [
    path('landlord/new', LandlordSignupView.as_view(), name='landlord_new'),
    path('renter/new', ProfileCreateView.as_view(), name='create_renter'),
]
