from django.shortcuts import render
from .forms import LatepaymentForm
from .models import Payment, Rent

# Create your views here.
def latepayment(request):
	if 'month' in request.GET:
		form = LatepaymentForm(request.GET)
		if form.is_valid():
			rent_ids = [payment.rent.id for payment in Payment.objects.filter(start__month=form.cleaned_data['month'], start__year=form.cleaned_data['year'])]
			not_paid_rent = Rent.objects.filter(active=True, start_date__month__lte=form.cleaned_data['month'], start_date__year__lte=form.cleaned_data['year']).exclude(id__in = rent_ids)
	else:
		not_paid_rent = {}
		form = LatepaymentForm()
	return render(request, 'house/latepayment.html', {'form': form, 'data': not_paid_rent})