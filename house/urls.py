from django.urls import path
from . import views

app_name = 'house'

urlpatterns = [
    path('add/', views.AddHouseView.as_view(), name='add'),
    path('list/', views.HouseListView.as_view(), name='list'),
    path('latepayment/', views.latepayment, name='latepayment'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
]