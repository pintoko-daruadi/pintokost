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

class Price(models.Model):
	nominal = models.PositiveIntegerField('Harga Sewa')
	active = models.BooleanField('Status Harga Aktif', default=True)

	def __str__(self):
		return "%s" % toRupiah(self.nominal)

class Rent(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Rumah')
	renter = models.ForeignKey(Renter, on_delete=models.PROTECT, verbose_name='Penyewa')
	price = models.ForeignKey(Price, on_delete=models.PROTECT, verbose_name='Harga', default=None)
	active = models.BooleanField('Status Sewa Aktif', default=True)

	def __str__(self):
		return "%s (%s/%s) - %saktif" % (self.house.name, self.renter.user.username, self.price, ('' if self.active else 'tidak '))

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	pay_date = models.DateField('Tanggal Bayar', default=None)
	start = models.DateField('Mulai Sewa')
	end = models.DateField('Akhir Sewa')

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
