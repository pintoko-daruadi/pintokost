from django import forms
from django.utils.dates import MONTHS
from .models import House

class HouseForm(forms.ModelForm):
	class Meta:
		model = House
		fields = ['name', 'address', 'pln_number', 'image']
		widgets = {
			'address': forms.Textarea(),
		}
		labels = {
			'name': 'Nama Rumah',
			'address': 'Alamat Lengkap',
		}
