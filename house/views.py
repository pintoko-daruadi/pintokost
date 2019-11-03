from django.shortcuts import render, redirect
from django.utils.dates import MONTHS
from .forms import LatepaymentForm
from .models import Payment, Rent

def index(request):
	return redirect('/admin/')

def latepayment(request):
	month = MONTHS[int(request.GET.get('month', '(bulan tidak valid)'))]
	year = request.GET.get('year', '(tahun tidak valid)')
	if 'month' in request.GET:
		form = LatepaymentForm(request.GET)
		if form.is_valid():
			rent_ids = Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year']).values_list('rent__id', flat=True)
			not_paid_rent = Rent.objects.filter(active=True, start_date__month__lte=form.cleaned_data['month'], start_date__year__lte=form.cleaned_data['year']).exclude(id__in = rent_ids).order_by('house')
			if not request.user.is_superuser:
				not_paid_rent = not_paid_rent.filter(house__owner__user=request.user)
	else:
		not_paid_rent = {}
		form = LatepaymentForm()
	return render(request, 'house/latepayment.html', {'form': form, 'data': not_paid_rent, 'month': month, 'year': year})
