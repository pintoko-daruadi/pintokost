from django.db import models
from django.conf import settings

# Create your models here.

class Renter(models.Model):
	"""docstring for Renter"""
	GENDER_CHOICES = (
		('M', 'Pria'),
		('F', 'Wanita'),
	)
	IDENTITY_TYPES = (
		('KTP', 'KTP - Kartu Tanda Penduduk'),
		('SIM', 'SIM - Surat Ijin Mengemudi'),
		('KTM', 'KTM - Kartu Tanda Mahasiswa'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Username Penyewa', default=None)
	identity_type = models.CharField('Jenis Identitas', max_length=3, choices=IDENTITY_TYPES)
	identity_number = models.CharField('Nomor Identitas', max_length=50)
	dob = models.DateField('Tanggal Lahir')
	gender = models.CharField('Jenis Kelamin', max_length=1, choices=GENDER_CHOICES)
	work = models.CharField('Pekerjaan', max_length=100)
	phone = models.CharField('Phone', max_length=100)

	def __str__(self):
		return "%s %s (%s) - %s" % (self.user.first_name, self.user.last_name, self.user.username, self.phone)

class Owner(models.Model):
	"""docstring for Owner"""
	GENDER_CHOICES = (
		('M', 'Pria'),
		('F', 'Wanita'),
	)
	IDENTITY_TYPES = (
		('KTP', 'KTP - Kartu Tanda Penduduk'),
		('SIM', 'SIM - Surat Ijin Mengemudi'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Username Pemilik', default=None)
	identity_type = models.CharField('Jenis Identitas', max_length=3, choices=IDENTITY_TYPES)
	identity_number = models.CharField('Nomor Identitas', max_length=50)
	dob = models.DateField('Tanggal Lahir')
	gender = models.CharField('Jenis Kelamin', max_length=1, choices=GENDER_CHOICES)
	work = models.CharField('Pekerjaan', max_length=100)
	phone = models.CharField('Phone', max_length=100)

	def __str__(self):
		return "%s %s (%s) - %s" % (self.user.first_name, self.user.last_name, self.user.username, self.phone)
		