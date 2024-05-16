from django import forms
from .models import House


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['name', 'address', 'pln_number', 'image']
        widgets = {
            'address': forms.Textarea({'rows': 4}),
        }
        labels = {
            'name': 'Nama Rumah',
            'address': 'Alamat Lengkap',
            'pln_number': 'Nomor listrik PLN',
        }
