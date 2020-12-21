from django import forms
from django.utils.dates import MONTHS
from datetime import date

class LatepaymentForm(forms.Form):
	START_SAVE_DATA = 2021
	years = [(x, str(x)) for x in range(START_SAVE_DATA, (date.today().year+1))]
	year = forms.ChoiceField(choices=years, widget=forms.Select(attrs={'onchange':'this.form.submit()'}))
	
	months = [(x, MONTHS[x]) for x in range(1, 13)]
	month = forms.ChoiceField(choices=months, widget=forms.Select(attrs={'onchange':'this.form.submit()'}))
