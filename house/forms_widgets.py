from django.contrib.auth.models import User
from django_select2 import forms as s2forms

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

class IndoPlaceWidget(s2forms.ModelSelect2Widget):
	search_fields = ['name__icontains']
	max_results = 2

	def build_attrs(self, base_attrs, extra_attrs):
		return super().build_attrs(base_attrs, extra_attrs={"data-minimum-input-length": 4})
