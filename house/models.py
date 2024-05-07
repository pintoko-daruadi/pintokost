from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

from pintokost.helpers import resize_image, toRupiah

def house_dir(instance, filename):
	return "house/{0}/{1}".format(instance.owner.username, filename)

class House(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=300)
	pln_number = models.CharField('Nomor listrik PLN', max_length=20, blank=True)
	active = models.BooleanField(default=True)
	deleted_at = models.DateTimeField(blank=True, null=True)
	owner = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		limit_choices_to={'groups__name': 'owner'}
	)
	image = models.ImageField(null=True, blank=True, upload_to=house_dir)

	def __str__(self):
		return self.name

	def image_url(self):
		if self.image and hasattr(self.image, 'url'):
			return self.image.url

		from django.templatetags.static import static
		return static('default.jpg')

	def save(self):
		if self.image:
			self.image = resize_image(self.image)

		super(House, self).save()

	def soft_delete(self):
		self.active = False
		self.deleted_at = timezone.now()
		self.save()

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
	start_date = models.DateField(default=datetime.date.today, help_text='Format: YYYY-MM-DD')
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

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	nominal = models.DecimalField(max_digits=12, default=0, decimal_places=2, verbose_name='Harga')
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
