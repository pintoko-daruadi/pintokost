from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages

from house.mixins import HouseOwnerMixin, HouseRentedMixin
from house.models import House
from rent.forms import RentForm
from rent.models import Rent

class RentCreateView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, HouseRentedMixin, CreateView):
	house = None
	form_class = RentForm
	model = Rent
	permission_required = 'house.add_rent'
	success_url = reverse_lazy('house:list')
	template_name = 'rent/form.html'

	def get_initial(self):
		self.house = get_object_or_404(House, id=self.kwargs.get('pk'), owner=self.request.user)
		return {
			'house': self.house
		}

	def get_context_data(self, **kwargs):
		context = super(RentCreateView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Tambah'
		context['house'] = self.house
		return context

	def form_valid(self, form):
		form.instance.billing_date = form.instance.start_date
		form.instance.house = House.objects.get(id=self.kwargs.get('pk'))
		messages.success(self.request, "Penyewa di "+str(form.instance.house)+" berhasil ditambah")
		return super(RentCreateView, self).form_valid(form)

class RentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Rent
	permission_required = 'house.change_rent'
	success_message = "Sewa Rumah berhasil dihapus"
	success_url = reverse_lazy('house:list')
	template_name = 'rent/delete.html'

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.soft_delete()
		messages.success(self.request, self.success_message)
		return HttpResponseRedirect(self.get_success_url())
