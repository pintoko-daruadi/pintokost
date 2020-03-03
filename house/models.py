from django.db import models
from django.conf import settings
from .helpers import *
from django.contrib.auth.models import User, Permission
import datetime

# Create your models here.

class House(models.Model):
	name = models.CharField('Nama', max_length=50)
	address = models.CharField('Alamat', max_length=300)
	pln_number = models.CharField('Nomor PLN', max_length=20)
	owner = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		limit_choices_to={'groups__name': 'owner'}
	)

	def __str__(self):
		return self.name 

class Rent(models.Model):
	renter = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		verbose_name='Penyewa',
		limit_choices_to={'groups__name': 'renter'}
	)
	house = models.ForeignKey(House, on_delete=models.PROTECT, verbose_name='Rumah')
	price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Harga')
	billing_date = models.DateField('Tanggal Tagihan', default=None)
	active = models.BooleanField('Status Sewa', default=True)
	start_date = models.DateField("Awal Masuk", default=datetime.date.today, help_text='Format: YYYY-MM-DD')

	def __str__(self):
		return "%s / %s <%s>" % (self.house.name, self.renter.profile, toRupiah(self.price))

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=12, default=0, decimal_places=2, verbose_name='Harga')
	pay_date = models.DateField('Tanggal Bayar', default=None, help_text='Format: YYYY-MM-DD')
	start = models.DateField('Mulai Sewa', default=None, help_text='Format: YYYY-MM-DD')

	def __str__(self):
		return "%s/%s (%s)" % (self.rent.house.name, self.start, self.rent.renter)

class ExpenseType(models.Model):
	name = models.CharField('Tipe Pengeluaran', max_length=50)
	owner = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		verbose_name='Pemilik Rumah',
		limit_choices_to={'groups__name': 'owner'}
	)
	def __str__(self):
		return self.name

class Expense(models.Model):
	house = models.ForeignKey(House, on_delete=models.PROTECT)
	nominal = models.PositiveIntegerField('Biaya Pengeluaran')
	date = models.DateField('Tanggal')
	expense_type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, default=1)
	remark = models.CharField('Catatan', max_length=200)
	receipt_photo = models.ImageField(blank=True, null=True, upload_to=photo_path)

	def get_upload_folder(self):
		return 'expense'

	def __str__(self):
		return "%s <%s> (%s)" % (self.expense_type, toRupiah(self.nominal), self.house)
