from django import template
from house.helpers import toRupiah
register = template.Library()
from django.utils.safestring import mark_safe
from django.utils.html import format_html

@register.filter(name='remain')
def remain(payment, price):
    html = "<p><i class='fa fa-tags' style='color: var(--orange)'></i> {}</p>".format(toRupiah(price))
    if payment:
        html += "<i class='fa fa-exclamation-triangle' style='color: var(--red)'></i> Cicilan:<ul>"
        for p in payment:
            html += "<li class='fa fa-tag' style='color: var(--primary)'> {date} &rsaquo; {nominal}</li>".format(date=p.pay_date.strftime("%d-%b-%Y"), nominal=toRupiah(p.nominal))
        html += "</ul>"
    return format_html(mark_safe(html))
