from .models import House
from django.http import HttpResponseForbidden

class HouseOwnerMixin:
	def dispatch(self, request, *args, **kwargs):
		if House.objects.filter(id = kwargs.get('pk'), owner = request.user):
			return super(HouseOwnerMixin, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseForbidden('House Doesn\'t Exists')
