from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.dates import MONTHS
from django.urls import reverse_lazy
from datetime import datetime
from .forms import LatepaymentForm
from .models import Payment, Rent, Expense
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
			not_paid_rent = Rent.objects.filter(active=True, start_date__month__lte=form.cleaned_data['month'], start_date__year__lte=form.cleaned_data['year']).exclude(id__in = rent_ids).order_by('house')
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
		'year': year
	}
	return render(request, 'house/monthly_report.html', data)
