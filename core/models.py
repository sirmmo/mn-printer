# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.sites.models import Site
from django.db import models

class Application(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    
    secret = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.name
        
class Printer(models.Model):
    application = models.ForeignKey(Application, related_name="printers")
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    validator = models.TextField(null=True, blank=True)
    validate = models.BooleanField(default=False)

    text_template = models.BooleanField(default=True)
    file_template = models.BooleanField(default=False)

    template = models.TextField(null=True, blank=True)
    template_file = models.URLField(null=True, blank=True)

    outputs = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
        
    @property
    def outs(self):
        return self.outputs.split(" ")
