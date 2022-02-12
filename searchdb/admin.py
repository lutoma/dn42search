from django.contrib import admin
from .models import Host, URL


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
	pass


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
	pass
