from django import forms
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dates import MONTHS
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from datetime import date
from .forms import LatepaymentForm, RentForm
from .mixins import HouseOwnerMixin, HouseRentedMixin
from .models import Payment, Rent, Expense, House
from .helpers import toRupiah

def index(request):
	return redirect(reverse_lazy('house:latepayment'))

@login_required
def latepayment(request):
	month = date.today().month
	year = date.today().year
	not_paid_rent = {}
	income = 0
	expense = 0
	balance = 0
	form = LatepaymentForm(initial = {'year': year, 'month': month})

	if request.method == "POST":
		form = LatepaymentForm(request.POST)
		if form.is_valid():
			rent_ids = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year']).values_list('rent__id', flat=True)
			not_paid_rent = Rent.objects.filter(active=True, start_date__lte=date(int(form.cleaned_data['year']), int(form.cleaned_data['month']), 15)).exclude(id__in = rent_ids).order_by('house')
			income = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year'])
			expense = Expense.objects.filter(date__month=form.cleaned_data['month'], date__year=form.cleaned_data['year'])
			if not request.user.is_superuser:
				not_paid_rent = not_paid_rent.filter(house__owner=request.user)
				income = income.filter(rent__house__owner=request.user)
				expense = expense.filter(house__owner=request.user)
			income = int(income.aggregate(Sum('price'))['price__sum'] or 0)
			expense = int(expense.aggregate(Sum('nominal'))['nominal__sum'] or 0)
			balance = income - expense
			month = MONTHS[int(form.cleaned_data['month'])]
			year = form.cleaned_data['year']

	data = {
		'form': form,
		'data': not_paid_rent,
		'income': toRupiah(income),
		'expense': toRupiah(expense),
		'balance': toRupiah(balance),
		'balance_css_class': 'info' if balance > 0 else 'danger',
		'month': month,
		'year': year,
		'menu_home': True,
	}

	return render(request, 'house/monthly_report.html', data)

class HouseCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = 'house.add_house'
	model = House
	fields = ('name', 'address', 'pln_number', 'image')
	template_name = 'house/form.html'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah %(name)s berhasil ditambah"

	def get_context_data(self, **kwargs):
		context = super(HouseCreateView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Tambah'
		return context

	def get_form(self, form_class=None):
		form = super(HouseCreateView, self).get_form(form_class)
		form.fields['address'].widget = forms.Textarea()
		return form

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(HouseCreateView, self).form_valid(form)

class HouseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, DeleteView):
	permission_required = 'house.delete_house'
	model = House
	template_name = 'house/delete.html'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah berhasil dihapus"

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		for rent in self.object.rent_set.filter(active=True):
			rent.soft_delete()
		self.object.soft_delete()
		messages.success(self.request, self.success_message)
		return HttpResponseRedirect(self.get_success_url())

class HouseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = 'house.view_house'
	model = House
	template_name = 'house/list.html'

	def get_context_data(self, **kwargs):
		context = super(HouseListView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		return context

	def get_queryset(self):
		return House.objects.filter(owner = self.request.user, active=True)

class HouseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, SuccessMessageMixin, UpdateView):
	permission_required = 'house.change_house'
	model = House
	fields = ['name', 'address', 'pln_number', 'image']
	template_name = 'house/form.html'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah %(name)s berhasil diperbarui"

	def get_context_data(self, **kwargs):
		context = super(HouseUpdateView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Ubah'
		return context

	def get_form(self, form_class=None):
		form = super(HouseUpdateView, self).get_form(form_class)
		form.fields['address'].widget = forms.Textarea()
		return form

class PaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	model = Payment
	permission_required = 'house.add_payment'
	fields = ['price', 'pay_date', 'start']
	rent = None
	success_message = "Pembayaran berhasil disimpan"

	def get_initial(self):
		self.rent = get_object_or_404(Rent, id=self.kwargs.get('pk'), house__owner=self.request.user)
		return {
			'rent': self.rent,
			'price': int(self.rent.price),
			'pay_date': timezone.now(),
			'start': date(self.kwargs.get('year'), self.kwargs.get('month'), 1)
		}

	def get_context_data(self, **kwargs):
		context = super(PaymentCreateView, self).get_context_data(**kwargs)
		context['rent'] = self.rent
		return context

	def get_form(self, form_class=None):
		form = super(PaymentCreateView, self).get_form(form_class)
		form.fields['price'].widget.attrs = {'step': 1000}
		return form

	def get_success_url(self):
		return reverse_lazy('house:latepayment')

	def form_valid(self, form):
		form.instance.rent = self.rent
		return super(PaymentCreateView, self).form_valid(form)

class RentCreateView(LoginRequiredMixin, PermissionRequiredMixin, HouseOwnerMixin, HouseRentedMixin, CreateView):
	permission_required = 'house.add_rent'
	model = Rent
	form_class = RentForm
	template_name = 'rent/form.html'
	success_url = reverse_lazy('house:list')
	house = None

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
	permission_required = 'house.change_rent'
	model = Rent
	template_name = 'rent/delete.html'
	success_url = reverse_lazy('house:list')
	success_message = "Sewa Rumah berhasil dihapus"

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.soft_delete()
		messages.success(self.request, self.success_message)
		return HttpResponseRedirect(self.get_success_url())

class ThanksView(LoginRequiredMixin, TemplateView):
	template_name = 'house/thanks.html'
