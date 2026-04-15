from django.contrib import admin

from .models import Analytics, AppConfiguration, CoachModuleAccess, Module

admin.site.register(Module)
admin.site.register(CoachModuleAccess)
admin.site.register(AppConfiguration)
admin.site.register(Analytics)
