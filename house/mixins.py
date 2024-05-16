from rent.models import Rent
from .models import House
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy


class HouseOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        if House.objects.filter(id=kwargs.get('house_id'), owner=request.user).exists():
            return super(HouseOwnerMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('House Doesn\'t Exists')


class HouseRentedMixin:
    def dispatch(self, request, *args, **kwargs):
        rent = Rent.objects.filter(house__id=kwargs.get('house_id'), active=True).order_by('id').first()
        if rent:
            return HttpResponseRedirect(reverse_lazy('house:rent_deactivate', kwargs={'pk': rent.id}))
        else:
            return super(HouseRentedMixin, self).dispatch(request, *args, **kwargs)
