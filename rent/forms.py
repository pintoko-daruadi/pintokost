from django import forms
from django_select2 import forms as s2forms

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
