from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils import timezone
from .helpers import toRupiah
from indoplaces.models import Village
import datetime, re, os

def expense_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	new_filename = "{}_{}" % (instance.house, instance.expense_type)
	new_filename = re.sub('[^A-Za-z]', '_', new_filename)
	return 'expense/%Y/%m/%d/{filename}{ext}'.format(filename=new_filename, ext= file_extension)

def house_dir(instance, filename):
	return "house/{0}/{1}".format(instance.owner.username, filename)

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
	village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

	def image_url(self):
		if self.image and hasattr(self.image, 'url'):
			return self.image.url

		from django.templatetags.static import static
		return static('default.jpg')

	def save(self):
		from .helpers import resize_image
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

	def get_debt(house_owner, year, month):
		return Rent.objects.select_related('renter').prefetch_related(models.Prefetch('payment_set', queryset=Payment.get_paid(house_owner, year, month))).filter(
			house__owner=house_owner,
			active=True,
			start_date__lte=datetime.date(int(year), int(month), 15), #ambil pengontrak yg mulai dibawah tanggal 15
		).exclude(id__in=Payment.get_paid(house_owner, year, month).filter(rent__price=models.F('paid_nominal')).values_list('rent_id', flat=True))

class Payment(models.Model):
	rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
	nominal = models.DecimalField(max_digits=12, default=0, decimal_places=2, verbose_name='Harga')
	pay_date = models.DateField('Tanggal Bayar', default=None, help_text='Format: YYYY-MM-DD')
	start = models.DateField('Mulai Sewa', default=None, help_text='Format: YYYY-MM-DD')

	def __str__(self):
		return "%s/%s (%s)" % (self.rent.house.name, self.start, self.rent.renter)

	def get_paid(house_owner, year, month):
		return Payment.objects.select_related('rent').annotate(paid_nominal=models.Sum('nominal')).filter(
			rent__house__owner=house_owner,
			rent__active=True,
			start__year=year,
			start__month=month,
		)

	def kuitansi_obj(year, month, renter_username, owner_username):
		return Payment.objects.select_related('rent__house__owner').get(
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

	def monthly_outcome(owner, year, month):
		qs = Expense.objects.filter(
			house__owner=owner,
			date__year=year,
			date__month=month,
		).aggregate(models.Sum('nominal'))

		return int(qs['nominal__sum'] or 0)
