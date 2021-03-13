from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.dates import MONTHS
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormView, DeleteView, UpdateView
from django.views.generic.list import ListView
from datetime import date
from .forms import PaymentListForm, RentForm, HouseForm
from .mixins import HouseOwnerMixin, HouseRentedMixin
from .models import Payment, Rent, Expense, House
from .helpers import toRupiah

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

class KuitansiView(DetailView):
	model=Payment
	template_name = 'house/kuitansi.html'

	def get_object(self):
		try:
			pk = self.kwargs.get('pk')
			slug = self.kwargs.get('slug')
			slug = slug.split('-')
			return Payment.kuitansi_obj(pk, slug[0], slug[1], slug[2], slug[3])
		except Exception as e:
			raise Http404(e)

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['month_name'] = MONTHS[int(self.get_object().start.month)]
		context['nominal'] = toRupiah(self.get_object().nominal)
		context['price'] = toRupiah(self.get_object().rent.price)
		return context

class PaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	fields = ['nominal', 'pay_date', 'start']
	model = Payment
	permission_required = 'house.add_payment'
	rent = None
	success_message = "Pembayaran berhasil disimpan"
	success_url = reverse_lazy('house:payment_list')

	def get_initial(self):
		self.rent = get_object_or_404(Rent, id=self.kwargs.get('pk'), house__owner=self.request.user)
		return {
			'rent': self.rent,
			'nominal': int(self.rent.price),
			'pay_date': timezone.now(),
			'start': date(self.kwargs.get('year'), self.kwargs.get('month'), 1)
		}

	def get_context_data(self, **kwargs):
		context = super(PaymentCreateView, self).get_context_data(**kwargs)
		context['rent'] = self.rent
		return context

	def get_form(self, form_class=None):
		form = super(PaymentCreateView, self).get_form(form_class)
		form.fields['nominal'].widget.attrs = {'step': 1000}
		return form

	def form_valid(self, form):
		form.instance.rent = self.rent
		return super(PaymentCreateView, self).form_valid(form)

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

class RentPaymentView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
	form_class = PaymentListForm
	permission_required = 'house.view_rent'
	template_name = 'rent/paid_and_debt.html'

	def build_data_context(self, context, year, month):
		context['menu_pembayaran'] = True
		context['month'] = month
		context['month_name'] = MONTHS[int(month)]
		context['year'] = year
		context['debt'] = Rent.get_debt(self.request.user, year, month)
		context['paid'] = Payment.get_paid(self.request.user, year, month)
		income = Payment.monthly_income(self.request.user, year, month)
		context['income'] = toRupiah(income)
		expense = Expense.monthly_outcome(self.request.user, year, month)
		context['expense'] = toRupiah(expense)
		balance = income - expense
		context['balance'] = toRupiah(balance)
		context['balance_css_class'] = 'info' if balance > 0 else 'danger'
		context['slug'] = str(year)+"-"+str(month)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		context = self.build_data_context(context, form.cleaned_data['year'], form.cleaned_data['month'])
		return super(RentPaymentView, self).render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super(RentPaymentView, self).get_context_data(**kwargs)
		today = date.today()
		context = self.build_data_context(context,today.year, today.month)
		return context

	def get_initial(self):
		return {
			'year': PaymentListForm.START_YEAR,
			'month': date.today().month,
		}

class ThanksView(LoginRequiredMixin, TemplateView):
	template_name = 'house/thanks.html'
