from django.contrib import admin
from .models_list import models_list


@admin.register(*models_list)
class BaseAdmin(admin.ModelAdmin):
    search_fields = ['uuid']
    date_hierarchy = 'created_at'
