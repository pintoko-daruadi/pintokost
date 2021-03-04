from django import forms
from django.utils.dates import MONTHS
from datetime import date
from django_select2 import forms as s2forms
from django.contrib.auth.models import User
from .models import House, Rent
from indoplaces.models import Province, Regency, District, Village

class RenterWidget(s2forms.ModelSelect2Widget):
	queryset = User.objects.filter(groups__name='renter')
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
	year = forms.ChoiceField(choices=years)

	months = [(x, MONTHS[x]) for x in range(1, 13)]
	month = forms.ChoiceField(choices=months)

class RentForm(forms.ModelForm):
	class Meta:
		model = Rent
		fields = ['renter', 'price', 'start_date']
		widgets = {
			'renter': RenterWidget(max_results = 2),
		}

	def __init__(self, *args, **kwargs):
		super(RentForm, self).__init__(*args, **kwargs)
		self.fields['price'].widget.attrs = {'step': '1000'}

class HouseForm(forms.ModelForm):
	province = forms.ModelChoiceField(
		label='Provinsi',
		required=False,
		queryset=Province.objects.all(),
		widget=s2forms.ModelSelect2Widget(
			model=Province,
			search_fields=['name__icontains'],
			max_results=2
		)
	)
	regency = forms.ModelChoiceField(
		label='Kota/Kabupaten',
		required=False,
		queryset=Regency.objects.all(),
		widget=s2forms.ModelSelect2Widget(
			model=Regency,
			search_fields=['name__icontains'],
			dependent_fields={'province': 'province'},
			max_results=2
		),
	)
	district = forms.ModelChoiceField(
		label='Kecamatan',
		required=False,
		queryset=District.objects.all(),
		widget=s2forms.ModelSelect2Widget(
			model=District,
			search_fields=['name__icontains'],
			dependent_fields={'regency': 'regency'},
			max_results=2
		),
	)

	class Meta:
		model = House
		fields = ['name', 'address', 'pln_number', 'image', 'province', 'regency', 'district', 'village']
		widgets = {
			'address': forms.Textarea(),
			'village': s2forms.ModelSelect2Widget(
				queryset=Village.objects.all(),
				search_fields=['name__icontains'],
				dependent_fields={'district': 'district'},
				max_results=2
			),
		}
		labels = {
			'village': 'Kelurahan/Desa',
		}
