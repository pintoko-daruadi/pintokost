from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms
from django.utils.dates import MONTHS


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
                Div(    HTML('<button type="submit" class="btn btn-primary"><i class="fa fa-search"></i> Cari</button>'), css_class='col'),
                css_class='row'
            )
        )