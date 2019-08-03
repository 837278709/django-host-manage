# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Host, BusinessLine

admin.site.register(Host)
admin.site.register(BusinessLine)
