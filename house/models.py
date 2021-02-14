from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils import timezone
from .helpers import toRupiah
import datetime, re, os

def expense_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	new_filename = "{}_{}" % (instance.house, instance.expense_type)
	new_filename = re.sub('[^A-Za-z]', '_', new_filename)
	return 'expense/%Y/%m/%d/{filename}{ext}'.format(filename=new_filename, ext= file_extension)

def house_dir(instance, filename):
	return 'house/{0}/{1}'.format(instance.owner.username, filename)

class House(models.Model):
	name = models.CharField('Nama', max_length=50)
	address = models.CharField('Alamat', max_length=300)
	pln_number = models.CharField('Nomor PLN', max_length=20)
	active = models.BooleanField(default=True)
	deleted_at = models.DateTimeField(blank=True, null=True)
	owner = models.ForeignKey(
		User,
		on_delete=models.PROTECT,
		limit_choices_to={'groups__name': 'owner'}
	)
	image = models.ImageField(null=True, blank=True, upload_to=house_dir)

	def save(self):
		import sys
		from PIL import Image
		from io import BytesIO
		from django.core.files.uploadedfile import InMemoryUploadedFile

		im = Image.open(self.image)
		basewidth = 200
		wpercent = basewidth/float(im.size[0])
		hsize = im.size[1]*wpercent
		size_f = (basewidth, int(hsize))
		im = im.resize(size_f, Image.NEAREST)

		output = BytesIO()
		im.save(fp=output, format='JPEG', quality=90)
		self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

		super(House, self).save()

	def __str__(self):
		return self.name

	def soft_delete(self):
		self.active = False
		self.deleted_at = timezone.now()
		self.save()

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
	deleted_at = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return "%s : %s <%s>" % (self.house.name, self.renter.get_full_name(), toRupiah(self.price))

	def soft_delete(self):
		self.active = False
		self.deleted_at = timezone.now()
		self.save()

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
	receipt_photo = models.FileField(blank=True, null=True, upload_to=expense_path)

	def __str__(self):
		return "%s <%s> (%s)" % (self.expense_type, toRupiah(self.nominal), self.house)
