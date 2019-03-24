from django.contrib import admin
from .models import *
from .helpers import *

# Register your models here.
class HouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'pln_number', 'address', 'owner')

	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='Owner').count() > 0:
				self.exclude = ('owner',)
		form = super().get_form(request, obj, **kwargs)
		return form

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(owner__user = request.user)

admin.site.register(House, HouseAdmin)

class RentAdmin(admin.ModelAdmin):
	list_display = ('house', 'penyewa', 'price', 'active', 'owner')

	def penyewa(self, model_obj):
		return "%s %s (%s)" % (model_obj.renter.user.first_name, model_obj.renter.user.last_name, model_obj.renter.phone)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'price':
			kwargs['queryset'] = Price.objects.filter(active=True).order_by('nominal')
			return db_field.formfield(**kwargs)
		elif db_field.name == 'house' and not request.user.is_superuser:
			kwargs['queryset'] = House.objects.filter(owner__user=request.user)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def owner(self, model_obj):
		return "%s %s (%s)" % (model_obj.house.owner.user.first_name, model_obj.house.owner.user.last_name, model_obj.house.owner.phone)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(house__owner__user = request.user)

admin.site.register(Rent, RentAdmin)

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('house_name', 'pay_date', 'start', 'harga', 'penyewa', 'owner')
	ordering = ('rent',)

	def harga(self, model_obj):
		return "%s" % model_obj.rent.price

	harga.short_description = 'Harga'
	harga.admin_order_field = 'rent__price'

	def penyewa(self, model_obj):
		return "%s %s" % (model_obj.rent.renter.user.first_name, model_obj.rent.renter.user.last_name)

	def owner(self, model_obj):
		return "%s %s (%s)" % (model_obj.rent.house.owner.user.first_name, model_obj.rent.house.owner.user.last_name, model_obj.rent.house.owner.phone)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(rent__house__owner__user = request.user)
		return qs

	def house_name(self, model_obj):
		return model_obj.rent.house

	house_name.short_description = 'Rumah'
	house_name.admin_order_field = 'rent'

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'rent' and not request.user.is_superuser:
			kwargs['queryset'] = Rent.objects.filter(house__owner__user=request.user)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Payment, PaymentAdmin)

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('house', 'remark', 'date', 'get_formated_nominal', 'receipt_number')

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(house__owner__user = request.user)

	def get_formated_nominal(self, model_obj):
		return toRupiah(model_obj.nominal)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'house' and not request.user.is_superuser:
			kwargs['queryset'] = House.objects.filter(owner__user=request.user)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	get_formated_nominal.short_description = 'Biaya'
	get_formated_nominal.admin_order_field = '-nominal'

admin.site.register(Expense, ExpenseAdmin)

class PriceAdmin(admin.ModelAdmin):
	list_display = ('get_formated_nominal', 'active')
	ordering = ('nominal',)

	def get_formated_nominal(self, obj):
		return toRupiah(obj.nominal)
	get_formated_nominal.short_description = 'Harga Sewa'
	get_formated_nominal.admin_order_field = '-nominal'

admin.site.register(Price, PriceAdmin)

admin.site.site_header = "Pintoko Rent House"
admin.site.site_title = "Pintoko Rent House CMS"
admin.site.index_title = "House Management"