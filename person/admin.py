from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import IdentityInfo
from .forms import UserCompleteNameField
from django.utils.safestring import mark_safe

class AuthUserInline(admin.TabularInline):
	model = get_user_model()

class IdentityInfoAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'identity_name', 'phone', 'is_renter', 'is_owner', 'identity_photo_')
	readonly_fields = ('identity_photo_',)
	ordering = ('-is_owner', '-is_renter')
	# inlines = [AuthUserInline, ]

	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['form_class'] = UserCompleteNameField
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def identity_photo_(self, obj):
		try:
			img_url = obj.identity_photo.url
		except:
			img_url = '/media/default.jpg'

		return mark_safe('<img src="{url}" width="300px" />'.format(
			url= img_url
			)
		)
admin.site.register(IdentityInfo, IdentityInfoAdmin)
