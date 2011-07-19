from website.models import *
from django.contrib import admin

class SisterAdmin(admin.ModelAdmin):
  list_display = ('full_name', 'class_year', 'status', 'residence')
  list_filter = ['class_year', 'status', 'residence']
  search_fields = ['user__first_name', 'user__last_name', 'user__email']

admin.site.register(Residence)
admin.site.register(Sister, SisterAdmin)