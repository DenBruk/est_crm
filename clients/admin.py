from django.contrib import admin

# Register your models here.
from clients.models import services,company,data

admin.site.register(services)
admin.site.register(company)
admin.site.register(data)
