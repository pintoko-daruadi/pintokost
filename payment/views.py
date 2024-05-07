from datetime import date, timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.utils.dates import MONTHS
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, FormView

from expense.models import Expense
from payment.forms import PaymentListForm
from payment.models import Payment
from pintokost.helpers import toRupiah
from rent.models import Rent

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
		context = self.build_data_context(context, today.year, today.month)
		return context

	def get_initial(self):
		return {
			'year': date.today().year,
			'month': date.today().month,
		}