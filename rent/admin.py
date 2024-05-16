from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.dates import MONTHS
from datetime import date

from house.models import House
from pintokost.helpers import toRupiah
from rent.models import Rent


class ActiveRentFilter(admin.SimpleListFilter):
    title = 'Penyewa Aktif'
    parameter_name = 'is_active'
    default_value = True

    def lookups(self, request, model_admin):
        return (
            (True, 'Aktif'),
            (False, 'Sudah Keluar')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(active=self.value())

        return queryset


class RentAdmin(admin.ModelAdmin):
    list_display = ('house', 'renter', 'start_date', 'tanggal_tagihan', 'harga', 'active', 'owner')
    ordering = ('-active', 'house')
    list_filter = (ActiveRentFilter,)

    def tanggal_tagihan(self, obj):
        return "%s" % obj.billing_date.strftime("%d")

    def owner(self, obj):
        return obj.house.owner

    def harga(self, obj):
        return "%s" % toRupiah(obj.price)

    def alamat(self, obj):
        return "%s" % obj.house.address

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.edit = True
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'house':
            house = House.objects
            if not request.user.is_superuser:
                house = house.filter(owner=request.user)
            rented_house_id = Rent.objects.filter(active=True).values_list('house__id', flat=True)
            house = house.exclude(id__in=rented_house_id)
            kwargs['queryset'] = house
        elif db_field.name == 'renter':
            kwargs['queryset'] = User.objects.filter(profile__parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(house__owner=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('house', 'renter')
        return self.readonly_fields


admin.site.register(Rent, RentAdmin)
