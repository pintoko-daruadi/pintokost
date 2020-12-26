from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('renter/add', views.ProfileCreateView.as_view(), name='add'),
]
