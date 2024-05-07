from datetime import date, datetime, timezone
from django.db import models
from django.contrib.auth.models import User

from house.models import House
from pintokost.helpers import toRupiah

class Rent(models.Model):
	renter = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		limit_choices_to={'groups__name': 'renter'}
	)
	house = models.ForeignKey(House, on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	billing_date = models.DateField(default=None)
	active = models.BooleanField(default=True)
	start_date = models.DateField(default=date.today(), help_text='Format: YYYY-MM-DD')
	deleted_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return "%s : %s <%s>" % (self.house.name, self.renter.get_full_name(), toRupiah(self.price))

	def soft_delete(self):
		self.active = False
		self.deleted_at = timezone.now()
		self.save()

	def get_sum_payment(self):
		if self.payment_set.count() > 0:
			return Payment.objects.values('rent').annotate(sum_payment=models.Sum('nominal')).get(
				rent__id=self.id,
				start__year=self.payment_set.first().start.year,
				start__month=self.payment_set.first().start.month
			)['sum_payment']
		else:
			from decimal import Decimal
			return Decimal('0')

	def show_debt(self):
		return (self.get_sum_payment() < self.price)

	def get_debt(house_owner, year, month):
		paid = Payment.get_paid(house_owner, year, month)
		return Rent.objects.prefetch_related(models.Prefetch('payment_set', queryset=paid)).filter(
			house__owner=house_owner,
			active=True,
			start_date__lte=datetime.date(int(year), int(month), 15), #ambil pengontrak yg mulai dibawah tanggal 15
		).exclude(id__in=paid.annotate(sum_payment=models.Sum('nominal')).filter(sum_payment=models.F('rent__price')).values_list('rent_id', flat=True))

