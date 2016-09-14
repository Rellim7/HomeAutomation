from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(door)
admin.site.register(openEvent)
admin.site.register(closeEvent)
