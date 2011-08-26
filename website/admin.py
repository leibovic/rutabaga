from website.models import *
from django.contrib import admin

# Sisters
class SisterAdmin(admin.ModelAdmin):
  list_display = ('full_name', 'class_year', 'status', 'residence')
  list_filter = ['class_year', 'status', 'residence']
  search_fields = ['user__first_name', 'user__last_name', 'user__email']

admin.site.register(Sister, SisterAdmin)
admin.site.register(Residence)

# Events
class EventAdmin(admin.ModelAdmin):
  list_display = ('name', 'date', 'points')

admin.site.register(Event, EventAdmin)

# Content
class ContentAdmin(admin.ModelAdmin):
  list_display = ('view', 'html')

admin.site.register(Content, ContentAdmin)
