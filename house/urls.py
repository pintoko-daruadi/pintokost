from django.urls import path

from house.views import HouseCreateView, HouseDeleteView, HouseListView, HouseUpdateView, ThanksView

app_name = 'house'

urlpatterns = [
    path('', HouseListView.as_view(), name='list'),
    path('add', HouseCreateView.as_view(), name='add'),
    path('delete/<int:house_id>', HouseDeleteView.as_view(), name='delete'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('update/<int:pk>', HouseUpdateView.as_view(), name='update'),
]
