from django.contrib import admin
from .models import Renter, Owner
from .forms import UserCompleteNameField
from django.utils.safestring import mark_safe

class RenterAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'phone', 'work', 'gender', 'dob', 'identity_type', 'identity_number', 'identity_photo_text')
	readonly_fields = ('identity_photo_text',)

	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['form_class'] = UserCompleteNameField
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def identity_photo_text(self, obj):
		try:
			img_url = obj.receipt_photo.url
		except:
			img_url = '/media/default.jpg'

		return mark_safe('<img src="{url}" width="300px" />'.format(
			url= img_url
			)
		)
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
