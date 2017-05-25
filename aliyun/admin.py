# encoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import admin
from django.template import loader
from .models import Host, Application


class AppsFilter(admin.SimpleListFilter):
    title = "应用"
    parameter_name = 'apps'

    def lookups(self, request, model_admin):
        print(dir(Host.application_set))
        print(Host.application_set.through)
        # apps = [app.app_name for app in model_admin.model.]
        return ""

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__id__exact=self.value())
        else:
            return queryset


class HostAdmin(admin.ModelAdmin):

    def get_apps(self, instance):
        apps = []
        for app in instance.application_set.all():
            apps.append(app)
        return apps
    get_apps.short_description = '应用'

    def generate_sshconfig(self, request, queryset):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="config"'
        print(list(queryset))
        t = loader.get_template('sshconfig')
        c = {
            'hosts': list(queryset),
        }
        response.write(t.render(c))
        self.message_user(request, "导出成功")
        return response
    generate_sshconfig.short_description = u'生成sshconfig文件'

    list_display = ('hostname', 'ipadd_internet', 'ipadd_internal', 'has_days', 'get_apps')
    search_fields = ('hostname', 'ipadd_internet', 'ipadd_internal',)
    readonly_fields = ('time_created', 'time_release',)
    list_filter = ('zone', 'status', AppsFilter)
    actions = ('generate_sshconfig',)
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = False


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'get_hosts']
    search_fields = ['app_name']
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = False

admin.site.register(Host, HostAdmin)
admin.site.register(Application, ApplicationAdmin)

