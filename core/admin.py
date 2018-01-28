# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import *

class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields=('secret',)

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Printer)