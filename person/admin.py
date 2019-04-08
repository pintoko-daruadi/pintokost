from django.contrib import admin
from .models import Renter, Owner
from .forms import UserCompleteNameField

class RenterAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'phone', 'work', 'gender', 'dob', 'identity_type', 'identity_number')
	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['form_class'] = UserCompleteNameField
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Renter, RenterAdmin)

class OwnerAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'phone', 'work', 'gender', 'dob', 'identity_type', 'identity_number')
	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['form_class'] = UserCompleteNameField
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Owner, OwnerAdmin)
