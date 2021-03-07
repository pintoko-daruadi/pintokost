from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.dates import MONTHS
from datetime import date
from .models import *
from .helpers import *
from profile.models import Profile

class ExpenseListByMonthFilter(admin.SimpleListFilter):
	title = 'Bulan Expense'
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
			return queryset.filter(date__month=month)
		return queryset

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('house', 'remark', 'date', 'get_formated_nominal', 'expense_type', 'owner', 'receipt_photo_text')
	readonly_fields = ('receipt_photo_text',)
	list_filter = [ExpenseListByMonthFilter, ]

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
		return qs.filter(house__owner = request.user)

	def get_formated_nominal(self, obj):
		return toRupiah(obj.nominal)
	get_formated_nominal.short_description = 'Biaya'
	get_formated_nominal.admin_order_field = '-nominal'

	def owner(self, obj):
		return obj.house.owner

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'house' and not request.user.is_superuser:
			kwargs['queryset'] = House.objects.filter(owner=request.user).order_by('name')
		if db_field == 'owner':
			kwargs['queryset'] = ExpenseType.objects.filter(owner=request.user).order_by('name')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Expense, ExpenseAdmin)

class HouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'pln_number', 'address', 'owner', 'active')
	ordering = ('name',)
	autocomplete_fields = ['owner']

	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='owner').count() > 0:
				self.readonly_fields = ('owner',)
		else:
			self.readonly_fields = ('village',)
		form = super().get_form(request, obj, **kwargs)
		return form

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(owner = request.user)

admin.site.register(House, HouseAdmin)

class YearListFilter(admin.SimpleListFilter):
	title = 'Tahun Sewa'
	parameter_name = 'year'
	default_value = None

	def lookups(self, request, model_admin):
		year_list = []
		for key in range(2020, (date.today().year+1)):
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
		for key in range(1,13):
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
		house_list = House.objects.filter(owner = request.user).order_by('name').values('id', 'name')
		house =  {(v['id'],v['name']) for v in house_list}
		return house

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(rent__house = self.value())
		return queryset

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('house_name', 'penyewa', 'start', 'pay_date', 'billing_date', 'harga', 'owner')
	ordering = ('rent__house__name','-start',)
	readonly_fields = ('nominal',)
	fields = ('rent', 'nominal', 'pay_date', 'start')
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
			return qs.filter(rent__house__owner = request.user)
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

class ExpenseTypeAdmin(admin.ModelAdmin):
	pass

admin.site.register(ExpenseType, ExpenseTypeAdmin)

admin.site.site_header = "Pintoko Rent House"
admin.site.site_title = "Pintoko Rent House CMS"
admin.site.index_title = "House Management"
