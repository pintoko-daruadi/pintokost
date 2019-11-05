from django.shortcuts import render, redirect
from django.utils.dates import MONTHS
from django.db.models import Sum
from datetime import datetime
from .forms import LatepaymentForm
from .models import Payment, Rent, Expense
from .helpers import toRupiah

def index(request):
	return redirect('/admin/')

def latepayment(request):
	month = MONTHS[int(request.GET.get('month', datetime.now().month))]
	year = request.GET.get('year', datetime.now().year)
	if 'month' in request.GET:
		form = LatepaymentForm(request.GET)
		if form.is_valid():
			rent_ids = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year']).values_list('rent__id', flat=True)
			not_paid_rent = Rent.objects.filter(active=True, start_date__month__lte=form.cleaned_data['month'], start_date__year__lte=form.cleaned_data['year']).exclude(id__in = rent_ids).order_by('house')
			income = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year'])
			outcome = Expense.objects.filter(date__month=form.cleaned_data['month'], date__year=form.cleaned_data['year'])
			if not request.user.is_superuser:
				not_paid_rent = not_paid_rent.filter(house__owner__user=request.user)
				income = income.filter(rent__house__owner__user=request.user)
				outcome = outcome.filter(house__owner__user=request.user)
			income = income.aggregate(Sum('price'))['price__sum']
			outcome = outcome.aggregate(Sum('nominal'))['nominal__sum']
	else:
		not_paid_rent = {}
		income = 0
		outcome = 0
		form = LatepaymentForm()
	balance = income - outcome
	data = {
		'form': form,
		'data': not_paid_rent,
		'income': toRupiah(income),
		'outcome': toRupiah(outcome),
		'balance': toRupiah(balance),
		'balance_css_class': 'info' if balance > 0 else 'danger',
		'month': month,
		'year': year
	}
	return render(request, 'house/monthly_report.html', data)
