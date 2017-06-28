from django.contrib import admin

# Register your models here.
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'port', 'created_at', 'updated_at')

admin.site.register(Client, ClientAdmin)

