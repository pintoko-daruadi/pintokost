from django.db import models
from django.conf import settings
from house.helpers import *

# Create your models here.

class IdentityInfo(models.Model):
	"""docstring for IdentityInfo"""
	GENDER = (
		('M', 'Pria'),
		('F', 'Wanita'),
	)
	IDENTITY_TYPES = (
		('KTP', 'KTP - Kartu Tanda Penduduk'),
		('SIM', 'SIM - Surat Ijin Mengemudi'),
		('KTM', 'KTM - Kartu Tanda Mahasiswa'),
	)
	RELIGION = (
		('islam', 'Islam'),
		('kristen', 'Kristen'),
		('hindu', 'Hindu'),
		('buddha', 'Buddha'),
		('konghucu', 'Konghucu'),
	)
	MARRIAGE_STATUS = (
		('menikah', 'Menikah'),
		('belum', 'Belum Menikah'),
	)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Username', default=None)
	identity_type = models.CharField('Jenis Identitas', max_length=3, choices=IDENTITY_TYPES)
	identity_number = models.CharField('Nomor Identitas', max_length=50)
	identity_name = models.CharField('Nama Sesuai Identitas', max_length=60, null=True)
	dob = models.DateField('Tanggal Lahir')
	gender = models.CharField('Jenis Kelamin', max_length=1, choices=GENDER)
	identity_address = models.CharField('Alamat Sesuai Identitas', max_length=100, null=True)
	religion = models.CharField('Agama', max_length=8, choices=RELIGION)
	marriage_status = models.CharField('Status Perkawinan', max_length=7, choices=MARRIAGE_STATUS)
	work = models.CharField('Pekerjaan', max_length=100)
	phone = models.CharField('Phone', max_length=100)
	is_renter = models.BooleanField('Penyewa', default=False)
	is_owner = models.BooleanField('Pemilik', default=False)
	identity_photo = models.ImageField(blank=True, null=True, upload_to=photo_path)

	def get_upload_folder(self):
		return 'identity'

	def __str__(self):
		return "%s %s (%s) - %s" % (self.user.first_name, self.user.last_name, self.user.username, self.phone)
