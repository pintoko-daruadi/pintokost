from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from crispy_forms.bootstrap import PrependedText
from django import forms
from django.utils.dates import MONTHS
from datetime import date
from .models import House, Rent
from indoplaces.models import Province, Regency, District, Village
from house.forms_widgets import RenterWidget, IndoPlaceWidget

class HouseForm(forms.ModelForm):
	province = forms.ModelChoiceField(
		label='Provinsi',
		required=False,
		queryset=Province.objects.all(),
		widget=IndoPlaceWidget(
			model=Province,
		)
	)
	regency = forms.ModelChoiceField(
		label='Kota/Kabupaten',
		required=False,
		queryset=Regency.objects.all(),
		widget=IndoPlaceWidget(
			model=Regency,
			dependent_fields={'province': 'province'},
		),
	)
	district = forms.ModelChoiceField(
		label='Kecamatan',
		required=False,
		queryset=District.objects.all(),
		widget=IndoPlaceWidget(
			model=District,
			dependent_fields={'regency': 'regency'},
		),
	)

	class Meta:
		model = House
		fields = ['name', 'province', 'regency', 'district', 'village', 'address', 'pln_number', 'image']
		widgets = {
			'address': forms.Textarea(),
			'village': IndoPlaceWidget(
				queryset=Village.objects.all(),
				dependent_fields={'district': 'district'},
			),
		}
		labels = {
			'name': 'Nama Rumah',
			'address': 'Alamat Lengkap',
			'village': 'Kelurahan/Desa',
		}

class PaymentListForm(forms.Form):
	START_YEAR = 2021
	years = [(x, str(x)) for x in range(START_YEAR, (date.today().year+1))]
	year = forms.ChoiceField(choices=years)

	months = [(x, MONTHS[x]) for x in range(1, 13)]
	month = forms.ChoiceField(choices=months)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.layout = Layout(
			Div(
				Div('year', css_class='col'),
				Div('month', css_class='col px-0'),
				Div(HTML('<button type="submit" class="btn btn-primary"><i class="fa fa-search"></i> Cari</button>'), css_class='col'),
				css_class='row'
			)
		)

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
