from django.contrib import admin
from .models import Renter, Owner

# Register your models here.
class RenterAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'phone', 'work', 'gender', 'dob', 'identity_type', 'identity_number')
	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
admin.site.register(Renter, RenterAdmin)

class OwnerAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama_lengkap', 'phone', 'work', 'gender', 'dob', 'identity_type', 'identity_number')
	def nama_lengkap(self, model_obj):
		return "%s %s" % (model_obj.user.first_name, model_obj.user.last_name)
admin.site.register(Owner, OwnerAdmin)