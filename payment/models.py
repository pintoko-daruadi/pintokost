from django.db import models

from pintokost.helpers import toRupiah
from rent.models import Rent

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	nominal = models.DecimalField(max_digits=12, default=0, decimal_places=2)
	pay_date = models.DateField('Tanggal Bayar', default=None, help_text='Format: YYYY-MM-DD')
	start = models.DateField('Mulai Sewa', default=None, help_text='Format: YYYY-MM-DD')

	def __str__(self):
		return "%s/%s (%s)" % (self.rent.house.name, self.start, self.rent.renter)

	def get_paid(house_owner, year, month):
		return Payment.objects.select_related('rent').filter(
			rent__house__owner=house_owner,
			rent__active=True,
			start__year=year,
			start__month=month,
		)

	def kuitansi_obj(pk, year, month, renter_username, owner_username):
		return Payment.objects.select_related('rent__house__owner').get(
			id = pk,
			rent__house__owner__username=owner_username,
			rent__renter__username=renter_username,
			start__year=year,
			start__month=month
		)

	def monthly_income(owner, year, month):
		qs = Payment.objects.filter(
			rent__house__owner=owner,
			start__year=year,
			start__month=month,
		).aggregate(models.Sum('nominal'))

		return int(qs['nominal__sum'] or 0)

	def nominal_in_rupiah(self):
		return toRupiah(self.nominal)

