from django import forms
from .models import Profile

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
