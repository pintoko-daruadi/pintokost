from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import format_lazy
from django_select2 import forms as s2forms

from rent.models import Rent


class RenterWidget(s2forms.ModelSelect2Widget):
    queryset = User.objects.filter(groups__name='renter')
    search_fields = [
        'first_name__icontains',
        'last_name__icontains',
    ]

    def label_from_instance(self, obj):
        masked_nik = len(obj.profile.nik[:-4]) * '#' + obj.profile.nik[-4:]
        return str(obj.get_full_name()).upper() + " - <NIK: " + masked_nik + ">"

    def build_attrs(self, base_attrs, extra_attrs):
        return super().build_attrs(base_attrs, extra_attrs={"data-minimum-input-length": 3})


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['renter', 'price', 'start_date']
        widgets = {
            'renter': RenterWidget(max_results=3),
            'price': forms.NumberInput(attrs={'step': '10000'}),
            'start_date': DatePickerInput()
        }
        labels = {
            'renter': 'Penyewa',
            'price': 'Harga per bulan',
            'start_date': 'Tanggal mulai sewa',
        }
        help_texts = {
            'renter': format_lazy('''
            Perhatikan nama dan 4 digit terakhir NIK untuk memastikan.
            Jika nama calon penyewa tidak ditemukan, gunakan menu <a href="{url}">Tambah Renter</a> untuk menambahkan.
            ''', url=reverse_lazy('profile:create_renter'))
        }
