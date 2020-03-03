from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserCompleteNameField
from django.utils.safestring import mark_safe

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = "Profile"
	fk_name = "user"

class ProfileAdmin(UserAdmin):
	list_display = ('user', 'group', 'parent', 'phone', 'identity_photo_')
	readonly_fields = ('identity_photo_',)
	inlines = (ProfileInline,)

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(ProfileAdmin, self).get_inline_instances(request, obj)

	def user(self, obj):
		return obj.username

	def parent(self, obj):
		return "--" or obj.profile.parent.username

	def phone(self, obj):
		return obj.profile.phone

	def group(self, obj):
		groups_list = obj.groups.values_list('name', flat=True)
		return list(groups_list)
	group.admin_order_field='groups__name'

	def identity_photo_(self, obj):
		try:
			img_url = obj.profile.photo_ktp.url
		except:
			img_url = '/media/default.jpg'

		return mark_safe('<img src="{url}" width="300px" alt="photo ktp" />'.format(url= img_url))

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
