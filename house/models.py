from django.db import models
from django.conf import settings
from .helpers import *
from person.models import IdentityInfo

# Create your models here.

class House(models.Model):
	name = models.CharField('Nama', max_length=50)
	address = models.CharField('Alamat', max_length=300)
	pln_number = models.CharField('Nomor PLN', max_length=20)
	owner = models.ForeignKey(
		IdentityInfo,
		on_delete=models.PROTECT,
		limit_choices_to={'is_owner': True}
	)

	def __str__(self):
		return self.name 

class Rent(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Rumah')
	renter = models.ForeignKey(
		IdentityInfo,
		on_delete=models.PROTECT,
		verbose_name='Penyewa',
		limit_choices_to={'is_renter': True}
	)
	price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Harga')
	billing_date = models.DateField('Tanggal Tagihan', default=None)
	active = models.BooleanField('Status Sewa Aktif', default=True)

	def __str__(self):
		return "%s / %s <%s>" % (self.house.name, self.renter.user.username, toRupiah(self.price))

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Harga')
	pay_date = models.DateField('Tanggal Bayar', default=None, help_text='Format: YYYY-MM-DD')
	start = models.DateField('Mulai Sewa', help_text='Format: YYYY-MM-DD')

	def __str__(self):
		return "%s/%s (%s)" % (self.rent.house.name, self.start.strftime("%B"), self.rent.renter.user.username)

class Expense(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT)
	nominal = models.PositiveIntegerField('Biaya Pengeluaran')
	date = models.DateField('Tanggal')
	remark = models.CharField('Catatan', max_length=200)
	receipt_number = models.CharField('Nomor Kwitansi', max_length=50)
	receipt_photo = models.ImageField(blank=True, null=True, upload_to=photo_path)

	def get_upload_folder(self):
		return 'expense'

	def __str__(self):
		return "%s %s (%s)" % (self.remark, toRupiah(self.nominal), self.house)
