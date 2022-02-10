from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Profile
from .forms import UserCompleteNameField

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = "Profile"
	fk_name = "user"

class ProfileAdmin(UserAdmin):
	list_display = ('user', 'group', 'parent', 'phone', 'identity_photo_', 'is_active')
	readonly_fields = ('identity_photo_',)
	inlines = (ProfileInline,)
	ordering = ('-is_active', 'username',)

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

		return mark_safe('<img src="{url}" width="250px" alt="photo ktp" />'.format(url= img_url))

	def get_fieldsets(self, request, obj=None):
		if not obj:
			return self.add_fieldsets

		if request.user.is_superuser:
			perm_fields = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
		else:
			# modify these to suit the fields you want your
			# staff user to be able to edit
			perm_fields = ('is_active', 'groups')

		return [
				(None, {'fields': ('username', 'password')}),
				(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
				(_('Permissions'), {'fields': perm_fields}),
				(_('Important dates'), {'fields': ('last_login', 'date_joined')})
		]

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)

# @admin.register(Profile)
# class ProfileOnlyAdmin(admin.ModelAdmin):
# 	list_display = ('user', 'nik')
