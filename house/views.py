from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import HouseForm
from .mixins import HouseOwnerMixin
from .models import House

def index(request):
	return redirect(reverse_lazy('house:payment_list'))

class HouseCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	form_class = HouseForm
	model = House
	permission_required = 'house.add_house'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah %(name)s berhasil ditambah"
	template_name = 'house/form.html'

	def get_context_data(self, **kwargs):
		context = super(HouseCreateView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Tambah'
		return context

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(HouseCreateView, self).form_valid(form)

class HouseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, DeleteView):
	model = House
	permission_required = 'house.delete_house'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah berhasil dihapus"
	template_name = 'house/delete.html'

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		for rent in self.object.rent_set.filter(active=True):
			rent.soft_delete()
		self.object.soft_delete()
		messages.success(self.request, self.success_message)
		return HttpResponseRedirect(self.get_success_url())

class HouseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = House
	permission_required = 'house.view_house'
	template_name = 'house/list.html'

	def get_context_data(self, **kwargs):
		context = super(HouseListView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		return context

	def get_queryset(self):
		return House.objects.filter(owner = self.request.user, active=True)

class HouseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, SuccessMessageMixin, UpdateView):
	form_class = HouseForm
	permission_required = 'house.change_house'
	model = House
	success_message = "Rumah %(name)s berhasil diperbarui"
	success_url = reverse_lazy('house:list')
	template_name = 'house/form.html'

	def get_context_data(self, **kwargs):
		context = super(HouseUpdateView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Ubah'
		return context

	def get_form(self, form_class=None):
		form = super(HouseUpdateView, self).get_form(form_class)
		if self.object.village and hasattr(self.object, 'village'):
			form.fields['province'].initial = self.object.village.district.regency.province_id
			form.fields['regency'].initial = self.object.village.district.regency_id
			form.fields['district'].initial = self.object.village.district_id
		return form

class ThanksView(LoginRequiredMixin, TemplateView):
	template_name = 'house/thanks.html'
