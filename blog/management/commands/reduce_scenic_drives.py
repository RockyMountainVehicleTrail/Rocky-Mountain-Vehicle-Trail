# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:32:47 2019

@author: mark
reduces the size of scenic drives to make the website load quicker
basically takes the 10th point along a lineString and makes a 'compressed'
LineString
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, LineString, MultiLineString

from blog.models import Picture, Post, Trail, ScenicDrive, State
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point
# import re, time, pickle, json, os, psycopg2, shutil



class Command(BaseCommand):
  
    def __init__(self):
        pass

    def handle(self, *args, **options):
        scenic_drives = ScenicDrive.objects.all()
        for sd in scenic_drives:
            
            print(sd.title)
            if not sd.reduced_multi_line_string:
                reduced_mls_list = []
                for ls in sd.multi_line_string:
                    if len(ls) <= 10:
                        pass
                    else:
                        print(len(ls))
                        coord_list = ls
                        point_list_line_string = []
                        for i in range(0, len(coord_list), 10):
                            point_list_line_string.append(coord_list[i])
                        reduced_mls_list.append(LineString(point_list_line_string))
                sd.reduced_multi_line_string = MultiLineString(reduced_mls_list)
                sd.save()
                print(sd.title + ' done')
        print('done')
                    
        


        
        
        
        
        
        