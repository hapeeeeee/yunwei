from django.contrib import admin
from hosts.models import Host

# Register your models here.

class HostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Host, HostAdmin)
