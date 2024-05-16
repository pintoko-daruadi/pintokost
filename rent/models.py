import datetime
from django.db import models
from django.contrib.auth.models import User

from house.models import House
from pintokost.helpers import toRupiah


class Rent(models.Model):
    renter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'groups__name': 'renter'}
    )
    house = models.ForeignKey(House, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    billing_date = models.DateField(default=None)
    active = models.BooleanField(default=True)
    start_date = models.DateField(default=datetime.date.today, help_text='Format: YYYY-MM-DD')
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s : %s <%s>" % (self.house.name, self.renter.get_full_name(), toRupiah(self.price))

    def soft_delete(self):
        self.active = False
        self.deleted_at = datetime.date.today
        self.save()
