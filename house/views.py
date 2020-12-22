from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.utils.dates import MONTHS
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from datetime import datetime
from .forms import LatepaymentForm, HouseForm
from .models import Payment, Rent, Expense, House
from .helpers import toRupiah

def index(request):
	return redirect(reverse_lazy('house:latepayment'))

@login_required
def latepayment(request):
	month = MONTHS[int(request.GET.get('month', datetime.now().month))]
	year = request.GET.get('year', datetime.now().year)
	if 'month' in request.GET:
		form = LatepaymentForm(request.GET)
		if form.is_valid():
			rent_ids = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year']).values_list('rent__id', flat=True)
			not_paid_rent = Rentt.objects.filter(active=True, start_date__month__lte=form.cleaned_data['month'], start_date__year__lte=form.cleaned_data['year']).exclude(id__in = rent_ids).order_by('house')
			income = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year'])
			expense = Expense.objects.filter(date__month=form.cleaned_data['month'], date__year=form.cleaned_data['year'])
			if not request.user.is_superuser:
				not_paid_rent = not_paid_rent.filter(house__owner__user=request.user)
				income = income.filter(rent__house__owner__user=request.user)
				expense = expense.filter(house__owner__user=request.user)
			income = income.aggregate(Sum('price'))['price__sum']
			expense = expense.aggregate(Sum('nominal'))['nominal__sum']
	else:
		not_paid_rent = {}
		income = 0
		expense = 0
		form = LatepaymentForm()
	income = 0 if income is None else income
	expense = 0 if expense is None else expense
	balance = income - expense
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

class HouseListView(LoginRequiredMixin, ListView):
	model = House
	template_name = 'house/list.html'

	def get_queryset(self):
		return House.objects.filter(owner = self.request.user)

	def get_context_data(self, **kwargs):
		context = super(HouseListView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		return context

class AddHouseView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = House
	fields = ('name', 'address', 'pln_number')
	template_name = 'house/form.html'
	success_url = reverse_lazy('house:list')
	success_message = "Rumah %(name)s - %(address)s berhasil ditambahkan"

	def get_context_data(self, **kwargs):
		context = super(AddHouseView, self).get_context_data(**kwargs)
		context['menu_house'] = True
		context['action'] = 'Tambah'
		return context
	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(AddHouseView, self).form_valid(form)

class ThanksView(LoginRequiredMixin, TemplateView):
	template_name = 'house/thanks.html'
