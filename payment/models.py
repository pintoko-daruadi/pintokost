from django.db import models

from house.models import House
from rent.models import Rent


def is_already_paid(house: House, year: int, month: int):
    return True


class Payment(models.Model):
    rent = models.ForeignKey(Rent, on_delete=models.PROTECT)
    nominal = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    pay_date = models.DateField(default=None, help_text='Format: YYYY-MM-DD')
    billing_date = models.DateField(default=None, help_text='Format: YYYY-MM-DD')

    objects = models.Manager()

    def __str__(self):
        return "%s/%s (%s)" % (self.rent.house.name, self.billing_date, self.rent.renter)

    @classmethod
    def get_paid(cls, house_owner, year, month):
        return cls.objects.select_related('rent').filter(
            rent__house__owner=house_owner,
            rent__active=True,
            start__year=year,
            start__month=month,
        )

    def kuitansi_obj(pk, year, month, renter_username, owner_username):
        return Payment.objects.select_related('rent__house__owner').get(
            id=pk,
            rent__house__owner__username=owner_username,
            rent__renter__username=renter_username,
            start__year=year,
            start__month=month
        )

    def monthly_income(owner, year, month):
        qs = Payment.objects.filter(
            rent__house__owner=owner,
            start__year=year,
            start__month=month,
        ).aggregate(models.Sum('nominal'))

        return int(qs['nominal__sum'] or 0)

    def nominal_in_rupiah(self):
        return toRupiah(self.nominal)

# def get_sum_payment_of_rent(self, rent: Rent):
# 	return Payment.objects.values('rent').annotate(sum_payment=models.Sum('nominal')).get(
# 		rent__id=rent.id,
# 		start__year=self.payment_set.first().start.year,
# 		start__month=self.payment_set.first().start.month
# 	)['sum_payment']

# def show_debt(self):
# 	return False

# def get_debt(house_owner, year, month):
# 	paid = Payment.get_paid(house_owner, year, month)
# 	return Rent.objects.prefetch_related(models.Prefetch('payment_set', queryset=paid)).filter(
# 		house__owner=house_owner,
# 		active=True,
# 		start_date__lte=datetime.date(int(year), int(month), 15), #ambil pengontrak yg mulai dibawah tanggal 15
# 	).exclude(id__in=paid.annotate(sum_payment=models.Sum('nominal')).filter(sum_payment=models.F('rent__price')).values_list('rent_id', flat=True))
