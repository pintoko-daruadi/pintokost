from datetime import date

from django.contrib import admin
from django.utils.dates import MONTHS

from house.models import House
from payment.models import Payment
from pintokost.helpers import toRupiah
from rent.models import Rent


class YearListFilter(admin.SimpleListFilter):
    title = 'Tahun Sewa'
    parameter_name = 'year'
    default_value = None

    def lookups(self, request, model_admin):
        year_list = []
        for key in range(2020, (date.today().year + 1)):
            year_list.append(
                (key, str(key))
            )
        return year_list

    def queryset(self, request, queryset):
        if self.value():
            year = int(self.value())
            return queryset.filter(start__year=year)
        return queryset


class MonthListFilter(admin.SimpleListFilter):
    title = 'Bulan Sewa'
    parameter_name = 'month'
    default_value = None

    def lookups(self, request, model_admin):
        month_list = []
        for key in range(1, 13):
            month_list.append(
                (key, MONTHS[key])
            )
        return month_list

    def queryset(self, request, queryset):
        if self.value():
            month = int(self.value())
            return queryset.filter(start__month=month)
        return queryset


class HouseListFilter(admin.SimpleListFilter):
    title = 'Rumah'
    parameter_name = 'house'
    default_value = None

    def lookups(self, request, model_admin):
        house_list = House.objects.filter(owner=request.user).order_by('name').values('id', 'name')
        house = {(v['id'], v['name']) for v in house_list}
        return house

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rent__house=self.value())
        return queryset


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('house_name', 'penyewa', 'billing_date', 'pay_date', 'billing_date', 'harga', 'owner')
    ordering = ('rent__house__name', '-billing_date',)
    readonly_fields = ('nominal',)
    fields = ('rent', 'nominal', 'pay_date', 'billing_date')
    list_filter = (MonthListFilter, YearListFilter, HouseListFilter)

    def billing_date(self, obj):
        return "%s" % obj.rent.billing_date.strftime("%d")

    billing_date.short_description = 'Tanggal Tagihan'

    def penyewa(self, obj):
        return "%s (%s)" % (obj.rent.renter, obj.rent.renter.profile.phone)

    def owner(self, obj):
        return obj.rent.house.owner

    def harga(self, obj):
        return "%s" % toRupiah(obj.nominal)

    harga.admin_order_field = 'price'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(rent__house__owner=request.user)
        return qs

    def house_name(self, obj):
        return obj.rent.house

    house_name.short_description = 'Rumah'
    house_name.admin_order_field = 'rent__house__name'

    def save_model(self, request, obj, form, change):
        obj.price = obj.rent.price
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'rent':
            rent = Rent.objects.filter(active=True)
            if not request.user.is_superuser:
                rent = rent.filter(house__owner=request.user)
            kwargs['queryset'] = rent.order_by('house__name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Payment, PaymentAdmin)
