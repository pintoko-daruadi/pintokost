from django.urls import path
from . import views

app_name = 'house'

urlpatterns = [
    path('<int:pk>/rent', views.RentCreateView.as_view(), name='rent'),
    path('<int:pk>/rent/deactivate', views.RentDeleteView.as_view(), name='rent_deactivate'),
    path('add/', views.HouseCreateView.as_view(), name='add'),
    path('delete/<int:pk>', views.HouseDeleteView.as_view(), name='delete'),
    path('list/', views.HouseListView.as_view(), name='list'),
    path('payment_list/', views.payment_list, name='payment_list'),
    path('pay/<int:pk>/<int:year>/<int:month>', views.PaymentCreateView.as_view(), name='pay'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('update/<int:pk>', views.HouseUpdateView.as_view(), name='update'),
]
