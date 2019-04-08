from django.db import models
from django.conf import settings
from .helpers import *
from person.models import Renter, Owner

# Create your models here.

class House(models.Model):
	name = models.CharField('Nama', max_length=50)
	address = models.CharField('Alamat', max_length=300)
	pln_number = models.CharField('Nomor PLN', max_length=20)
	owner = models.ForeignKey(Owner, on_delete=models.PROTECT)

	def __str__(self):
		return self.name 

class Rent(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Rumah')
	renter = models.ForeignKey(Renter, on_delete=models.PROTECT, verbose_name='Penyewa')
	price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Harga')
	billing_date = models.DateField('Tanggal Tagihan', default=None)
	active = models.BooleanField('Status Sewa Aktif', default=True)

	def __str__(self):
		return "%s / %s <%s>" % (self.house.name, self.renter.user.username, toRupiah(self.price))

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Harga')
	pay_date = models.DateField('Tanggal Bayar', default=None)
	start = models.DateField('Mulai Sewa')

	def __str__(self):
		return "%s/%s (%s)" % (self.rent.house.name, self.start.strftime("%B"), self.rent.renter.user.username)

class Expense(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT)
	nominal = models.PositiveIntegerField('Biaya Pengeluaran')
	date = models.DateField('Tanggal')
	remark = models.CharField('Catatan', max_length=200)
	receipt_number = models.CharField('Nomor Kwitansi', max_length=50)

	def __str__(self):
		return "%s %s (%s)" % (self.remark, toRupiah(self.nominal), self.house)
