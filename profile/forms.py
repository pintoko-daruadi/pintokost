from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .models import Profile

class UserCompleteNameField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s" % (obj.first_name, obj.last_name, obj.username)

class LandlordSignupForm(UserCreationForm):
	full_name = forms.CharField(max_length=30, required=True, help_text='Harap gunakan nama lengkap sesuai KTP')
	email = forms.EmailField(max_length=256, required=True, help_text='Harap gunakan email aktif Anda')

	def save(self, commit=True, *args, **kwargs):
		user = super(LandlordSignupForm, self).save(commit=False, *args, **kwargs)
		split_name = self.cleaned_data.get('full_name').split()
		if len(split_name) > 1:
			user.first_name = " ".join(split_name[:len(split_name)-1])
			user.last_name = split_name[-1]
		else:
			user.first_name = split_name[0]
			user.last_name = split_name[0]
		user.username = (user.first_name[0]+user.last_name).lower() + self.cleaned_data.get('nik')[-4:]
		user.save()
		renter_group, created = Group.objects.get_or_create(name = 'owner')
		user.groups.add(renter_group)
		user.profile.nik = "-"
		user.profile.occupation = "-"
		user.profile.phone = "-"
		user.profile.save()

		return user

	class Meta:
		model = User
		fields = ['full_name', 'email', 'password1', 'password2']

class RenterForm(forms.ModelForm):
	full_name = forms.CharField(required=True, help_text='Harap gunakan nama lengkap sesuai KTP')
	nik = forms.CharField(required=True, help_text='Silahkan gunakan NIK pada KTP', label='NIK')
	occupation = forms.CharField(required=True, label='Pekerjaan')
	phone = forms.CharField(required=True, label='Nomor HP')

	def clean_nik(self):
		nik = self.cleaned_data.get('nik')

		if len(nik) != 16:
			raise forms.ValidationError('NIK KTP harus 16 digit')

		if not str(nik).isnumeric():
			raise forms.ValidationError('NIK KTP harus diisi angka')

		return nik

	def save(self, commit=True, *args, **kwargs):
		user = super(RenterForm, self).save(commit=False, *args, **kwargs)
		split_name = self.cleaned_data.get('full_name').split()
		if len(split_name) > 1:
			user.first_name = " ".join(split_name[:len(split_name)-1])
			user.last_name = split_name[-1]
		else:
			user.first_name = split_name[0]
			user.last_name = split_name[0]
		user.username = (user.first_name[0]+user.last_name).lower() + self.cleaned_data.get('nik')[-4:]
		user.save()
		renter_group, created = Group.objects.get_or_create(name = 'renter')
		user.groups.add(renter_group)
		user.profile.nik = self.cleaned_data.get('nik')
		user.profile.occupation = self.cleaned_data.get('occupation')
		user.profile.phone = self.cleaned_data.get('phone')
		user.profile.save()

		return user

	class Meta:
		model = User
		fields = ['nik', 'full_name', 'phone', 'occupation']
