# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:23:10 2019

@author: mark
"""

# from django.core.management.base import BaseCommand, CommandError
from blog.models import (Picture)
# from django.contrib.gis.geos import Point, LineString
# from haversine import haversine
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.gis.measure import D, Distance
from django import forms

class PictureForm(forms.Form):
    
    rotate_choices = [('0', 0),
                    ('90', 90),
                    ('180', 180),
                    ('270', 270)]
    description = forms.CharField(required=False)
    delete = forms.BooleanField(required=False)
    pic_id = forms.IntegerField(required=False)
    rotate = forms.ChoiceField(choices=rotate_choices, required=False)
#    pic_date = forms.DateInput()
    















