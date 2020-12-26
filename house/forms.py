from django import forms
from django.utils.dates import MONTHS
from datetime import date
from django_select2 import forms as s2forms
from .models import Rent

class PenghuniWidget(s2forms.ModelSelect2Widget):
	search_fields = [
		'first_name__icontains',
		'last_name__icontains',
	]

	def label_from_instance(self, obj):
		masked_nik = len(obj.profile.nik[:-4])*'#'+obj.profile.nik[-4:]
		return str(obj.get_full_name()).upper() + " - <NIK: " + masked_nik + ">"

class LatepaymentForm(forms.Form):
	START_SAVE_DATA = 2021
	years = [(x, str(x)) for x in range(START_SAVE_DATA, (date.today().year+1))]
	year = forms.ChoiceField(choices=years, widget=forms.Select(attrs={'onchange':'this.form.submit()'}))

	months = [(x, MONTHS[x]) for x in range(1, 13)]
	month = forms.ChoiceField(choices=months, widget=forms.Select(attrs={'onchange':'this.form.submit()'}))

class RentForm(forms.ModelForm):
	class Meta:
		model = Rent
		fields = ['renter', 'price', 'start_date']
		widgets = {
			'renter': PenghuniWidget,
		}

	def __init__(self, *args, **kwargs):
		super(RentForm, self).__init__(*args, **kwargs)
		self.fields['price'].widget.attrs = {'step': '1000'}
