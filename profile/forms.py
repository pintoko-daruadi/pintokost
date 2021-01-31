from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LandlordSignupForm(forms.ModelForm):
	full_name = forms.CharField(max_length=30, required=True)
	email = form.EmailField(max_length=256, required=True, help_text='Harap Gunakan Email Aktif Anda')
	nik = form.IntegerField(required=True)

	def save(self, commit=True, *args, **kwargs):
		user = super(LandlordSignupForm, self).save(commit=False, *args, **kwargs)
		split_name = self.cleaned_data.get('full_name').split()
		if len(split_name) > 1:
			user.first_name = " ".join(split_name[:-1])
			user.last_name = split_name[-1:]
		else:
			user.first_name = split_name[0]
			user.last_name = split_name[0]
		user.save()
		user.profile.nik = self.cleaned_data.get('nik')
		user.profile.save()

		return user

	class Meta:
		model = User
		fields = ['email', 'password1', 'password2']

class UserCompleteNameField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s - %s" % (obj.first_name, obj.last_name, obj.username)

class RenterForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['nik', 'occupation', 'phone']

	def clean_nik(self):
		nik = self.cleaned_data.get('nik')

		if len(nik) < 5:
			raise forms.ValidationError('NIK KTP minimal 5 digit')

		if not str(nik).isnumeric():
			raise forms.ValidationError('NIK KTP harus diisi angka')

		return nik

	first_name = forms.CharField(label='Nama Depan', required=True)
	last_name = forms.CharField(label='Nama Belakang', required=True)

	field_order = ['nik', 'first_name', 'last_name', 'phone', 'occupation']
