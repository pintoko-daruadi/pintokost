from django.contrib import admin
from .models import Province, Regency, District, Village

admin.site.register(Province)
admin.site.register(Regency)
admin.site.register(District)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    search_fields = ['name']
