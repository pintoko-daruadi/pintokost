from django.urls import path
from . import views

app_name = 'house'

urlpatterns = [
    path('<int:pk>/rent', views.RentCreateView.as_view(), name='rent'),
    path('add/', views.HouseCreateView.as_view(), name='add'),
    path('update/<int:pk>', views.HouseUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.HouseDeleteView.as_view(), name='delete'),
    path('list/', views.HouseListView.as_view(), name='list'),
    path('latepayment/', views.latepayment, name='latepayment'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
]