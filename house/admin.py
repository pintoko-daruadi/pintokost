from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.dates import MONTHS
from datetime import date
from .models import *
from .helpers import *

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('house', 'get_formated_nominal', 'remark', 'date', 'receipt_number', 'owner', 'receipt_photo_text')
	readonly_fields = ('receipt_photo_text',)

	def receipt_photo_text(self, obj):
		try:
			img_url = obj.receipt_photo.url
		except:
			img_url = '/media/default.jpg'

		return mark_safe('<img src="{url}" width="300px" />'.format(
			url= img_url
			)
		)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(house__owner__user = request.user)

	def get_formated_nominal(self, obj):
		return toRupiah(obj.nominal)
	get_formated_nominal.short_description = 'Biaya'
	get_formated_nominal.admin_order_field = '-nominal'

	def owner(self, obj):
		return obj.house.owner

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'house' and not request.user.is_superuser:
			kwargs['queryset'] = House.objects.filter(owner__user=request.user)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Expense, ExpenseAdmin)

class HouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'pln_number', 'address', 'owner')

	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='Owner').count() > 0:
				self.readonly_fields = ('owner',)
		else:
			self.readonly_fields = []
		form = super().get_form(request, obj, **kwargs)
		return form

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(owner__user = request.user)

admin.site.register(House, HouseAdmin)

class YearListFilter(admin.SimpleListFilter):
	title = 'Tahun Sewa'
	parameter_name = 'year'
	default_value = None

	def lookups(self, request, model_admin):
		year_list = []
		for key in range(2019, (date.today().year+1)):
			year_list.append(
				(key, str(key))
			)
		return year_list

	def queryset(self, request, queryset):
		if self.value():
			year = int(self.value())
			return queryset.filter(start__year__gte=year, start__year__lt=(year+1))
		return queryset

class MonthListFilter(admin.SimpleListFilter):
	title = 'Bulan Sewa'
	parameter_name = 'month'
	default_value = None

	def lookups(self, request, model_admin):
		month_list = []
		for key in range(1,13):
			month_list.append(
				(key, MONTHS[key])
			)
		return month_list

	def queryset(self, request, queryset):
		if self.value():
			month = int(self.value())
			return queryset.filter(start__month__gte=month, start__month__lt=(month+1))
		return queryset

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('house_name', 'penyewa', 'start', 'pay_date', 'billing_date', 'harga', 'owner')
	ordering = ('-start', 'rent__house__name',)
	readonly_fields = ('price',)
	fields = ('rent', 'price', 'pay_date', 'start')
	list_filter = (MonthListFilter, YearListFilter)

	def billing_date(self, obj):
		return "%s" % obj.rent.billing_date.strftime("%d")
	billing_date.short_description = 'Tanggal Tagihan'

	def penyewa(self, obj):
		return "%s %s (%s)" % (obj.rent.renter.user.first_name, obj.rent.renter.user.last_name, obj.rent.renter.phone)

	def owner(self, obj):
		return "%s %s (%s)" % (obj.rent.house.owner.user.first_name, obj.rent.house.owner.user.last_name, obj.rent.house.owner.phone)

	def harga(self, obj):
		return "%s" % toRupiah(obj.price)
	harga.admin_order_field = 'price'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(rent__house__owner__user = request.user)
		return qs

	def house_name(self, obj):
		return obj.rent.house
	house_name.short_description = 'Rumah'
	house_name.admin_order_field = 'rent__house__name'

	def save_model(self, request, obj, form, change):
		obj.price = obj.rent.price
		super().save_model(request, obj, form, change)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'rent' and not request.user.is_superuser:
			kwargs['queryset'] = Rent.objects.filter(house__owner__user=request.user, active=True)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Payment, PaymentAdmin)

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
			return queryset.filter(active = self.value())

		return queryset

class RentAdmin(admin.ModelAdmin):
	list_display = ('house', 'penyewa', 'alamat', 'tanggal_tagihan', 'harga', 'active', 'owner')
	ordering = ('-active', 'house')
	list_filter = (ActiveRentFilter,)

	def tanggal_tagihan(self, obj):
		return "%s" % obj.billing_date.strftime("%d")

	def penyewa(self, obj):
		return "%s %s (%s)" % (obj.renter.user.first_name, obj.renter.user.last_name, obj.renter.phone)

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
		if db_field.name == 'house' and not request.user.is_superuser:
			owner_house = House.objects.filter(owner__user=request.user)
			kwargs['queryset'] = owner_house
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(house__owner__user = request.user)
		return qs

admin.site.register(Rent, RentAdmin)

admin.site.site_header = "Pintoko Rent House"
admin.site.site_title = "Pintoko Rent House CMS"
admin.site.index_title = "House Management"
