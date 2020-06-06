from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

def profile_path(instance, filename):
	basefilename, file_extension= os.path.splitext(filename)
	return 'identity/{name}{ext}'.format(name= instance.user.username, ext= file_extension)

class Profile(models.Model):
	"""docstring for Profile"""
	GENDER = (
		('M', 'Pria'),
		('F', 'Wanita'),
	)

	user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Username', default=None)
	parent = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Kepala Keluarga', null=True, blank=True, related_name='children')
	nik = models.CharField('NIK KTP', max_length=50)
	occupation = models.CharField('Pekerjaan', max_length=100)
	phone = models.CharField('Phone', max_length=100)
	bank_account = models.CharField('Bank', max_length=10, help_text='Bank yang digunakan', null=True, blank=True)
	bank_account_number = models.CharField('Nomor Rekening', max_length=50, help_text='Nomor rekening bank yang digunakan', null=True, blank=True)
	photo_ktp = models.FileField(blank=True, null=True, upload_to=profile_path)

	def get_photo_ktp(self):
		try:
			return self.photo_ktp.url
		except:
			return '/media/default.jpg'

	def __str__(self):
		return "%s [%s]" % (self.user, self.phone)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
