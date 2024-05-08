from django import forms
from django_select2 import forms as s2forms
from django.contrib.auth.models import User
from datetime import date
from django.utils.dates import MONTHS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML

from rent.models import Rent

class RenterWidget(s2forms.ModelSelect2Widget):
	queryset = User.objects.filter(groups__name='renter')
	search_fields = [
		'first_name__icontains',
		'last_name__icontains',
	]

	def label_from_instance(self, obj):
		masked_nik = len(obj.profile.nik[:-4])*'#'+obj.profile.nik[-4:]
		return str(obj.get_full_name()).upper() + " - <NIK: " + masked_nik + ">"

	def build_attrs(self, base_attrs, extra_attrs):
		return super().build_attrs(base_attrs, extra_attrs={"data-minimum-input-length": 4})

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

class PaymentListForm(forms.Form):
	START_YEAR = 2021
	year_range = reversed(range(START_YEAR, date.today().year+1))
	year_tuple = [(x, str(x)) for x in year_range]
	year = forms.ChoiceField(choices=year_tuple)

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