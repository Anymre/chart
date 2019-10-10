from django.contrib import admin

# Register your models here.
from sth.models import Forward, Back


class ModelAdminC(admin.ModelAdmin):
    list_display = ('date', 'now', 'price')
    ordering = ('date', 'now')
    list_filter = ('date', 'now')


admin.site.register(Forward, ModelAdminC)
admin.site.register(Back, ModelAdminC)
