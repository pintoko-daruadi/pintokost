from django.urls import path
from . import views

app_name = 'house'

urlpatterns = [
    path('latepayment/', views.latepayment, name='latepayment'),
]