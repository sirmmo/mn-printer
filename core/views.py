# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse

import json

from .models import *

# Create your views here.

def print_data(request, application, printer, form):
    try:
        data = json.loads(request.body)
        p = Printer.objects.get(slug=printer, application__slug=application)
        
        r = render_data(data, p)
        
        o = generate_out(form, p)
        
        return create_response(o, form)
        
    except Exception as ex:
        return HttpResponseBadRequest(ex)
        
        

def render_data(data, printer):
    if printer.file_template:
        return render_data_file(data, printer)
    elif printer.text_template:
        return render_data_text(data, printer)
    raise Exception("misconfiguration")