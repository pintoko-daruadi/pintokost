from django.contrib import admin
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

from expense.models import Expense, ExpenseType
from house.models import House
from pintokost.helpers import toRupiah

class ExpenseTypeAdmin(admin.ModelAdmin):
	pass
admin.site.register(ExpenseType, ExpenseTypeAdmin)

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

		return mark_safe('<img src="{url}" width="300px" />'.format(url= img_url))

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
