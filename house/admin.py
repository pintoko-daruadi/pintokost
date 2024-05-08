from django.contrib import admin
from django.utils.dates import MONTHS

from expense.models import Expense, ExpenseType
from pintokost.helpers import toRupiah
from .models import *
from profile.models import Profile

class HouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'pln_number', 'address', 'owner', 'active')
	ordering = ('name',)
	autocomplete_fields = ['owner']

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if request.user.groups.filter(name='owner').count() > 0:
			form.base_fields['owner'].queryset = User.objects.filter(username=request.user.username)
			form.base_fields['owner'].initial = request.user
		return form

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(owner = request.user)
admin.site.register(House, HouseAdmin)

admin.site.site_header = "Pintoko Rent House"
admin.site.site_title = "Pintoko Rent House CMS"
admin.site.index_title = "House Management"
