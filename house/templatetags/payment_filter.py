import datetime

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from house.models import House
from payment.models import Payment
from pintokost.helpers import toRupiah
from rent.models import Rent

register = template.Library()


@register.filter(name='remain')
def remain(payment, price):
    html = "<p><i class='fa fa-tags' style='color: var(--orange)'></i> {}</p>".format(toRupiah(price))
    html += "<i class='fa fa-exclamation-triangle' style='color: var(--red)'></i> Cicilan:<ul>"
    if payment:
        for p in payment:
            html += "<li style='color: var(--primary)'> {date} &rsaquo; {nominal}</li>".format(
                date=p.pay_date.strftime("%d-%b-%Y"), nominal=toRupiah(p.nominal))
    else:
        html += "<li><i> Belum ada pembayaran</i></li>"
    html += "</ul>"

    return format_html(mark_safe(html))


@register.simple_tag
def is_paid(house: House, year: int, month: int) -> bool:
    rent = Rent.objects.get(
        active=True,
        house=house
    )

    year = datetime.date.year if year is None else year
    month = datetime.date.month if month is None else month

    e = Payment.objects.filter(
        rent=rent,
        billing_date__month=month,
        billing_date__year=year,
    ).exists()
    return e
