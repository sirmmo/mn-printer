# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.template import engines, TemplateSyntaxError, Template, Context

import requests
import json

from .models import
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def list_printers(request, application):
    printers = Printer.objects.filter(application__slug=application)
    ret = []
    for p in printers:
        ret.append( {
            "slug":p.slug,
            "template": p.template,
            "name":p.name})
    return HttpResponse(json.dumps(ret))
    
    

@csrf_exempt
def print_data(request, application, printer, form):
    data = json.loads(request.body)
    p = Printer.objects.get(slug=printer, application__slug=application)
    return render_printer(p, form, data)
    
        
def template_from_string(template_string):
    chain = []
    for engine in engines.all():
        try:
            return engine.from_string(template_string)
        except TemplateSyntaxError as e:
            chain.append(e)
    raise TemplateSyntaxError()
        
def render_printer(printer, form, data):
    if form in ["html", "pdf"]:
        t = template_from_string(printer.template)
        c = {"data":data}
        if form == "html":
            res = HttpResponse(t.render(c))
            res["Access-Control-Allow-Origin"] = "*"
            return res
        elif form == "pdf":
            requests_response = requests.post("http://weasy:5001/pdf?filename={}.pdf".format(printer.slug), data=t.render(c))
            django_response = HttpResponse(
                content=requests_response.content,
                status=requests_response.status_code,
                content_type=requests_response.headers['Content-Type']
            )

            django_response["Access-Control-Allow-Origin"] = "*"
            return django_response
            
        pass
    elif form == "docx":
        #whoops
        pass