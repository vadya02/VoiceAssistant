from django.contrib import admin

from .models import Dashboards, Filters, FilterValues, RequestHistory

# Register your models here.
admin.site.register(RequestHistory)
admin.site.register(Filters)
admin.site.register(FilterValues)
admin.site.register(Dashboards)

