from django.contrib import admin
from django.db import models
from .models import Host


class HostAdmin(admin.ModelAdmin):
    list_display = ('vm_name', 'vm_ip', 'apps_list')
    search_fields = ['vm_ip', 'apps_list']
    list_editable = ['vm_ip', 'apps_list']
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = False

admin.site.register(Host, HostAdmin)
