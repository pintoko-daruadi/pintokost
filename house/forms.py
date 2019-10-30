from django import forms
from django.utils.dates import MONTHS
from datetime import date

class LatepaymentForm(forms.Form):
	years = [(x, str(x)) for x in range(2019, (date.today().year+1))]
	year = forms.ChoiceField(choices=years)
	
	months = [(x, MONTHS[x]) for x in range(1, 13)]
	month = forms.ChoiceField(choices=months, widget=forms.Select(attrs={'onchange':'this.form.submit()'}))
	
