# -*- coding: utf-8 -*-
"""
Reduce the size of recorded tracks.  
Hard set at one point in 100 as that works well.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, LineString

from blog.models import Picture, Post, Trail
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    
    def __init__(self):
        pass
        
    def handle(self, *args, **options):
#        print('hello there uncomment to run')
        trails = Trail.objects.all()
        
        for trail in trails:
            if not trail.reduced_line_string:
                print(trail.title)
                coord_list = trail.line_string.coords
                point_list_line_string = []
                for i in range(0, len(coord_list), 100):
                    point_list_line_string.append(coord_list[i])
                trail.reduced_line_string = LineString(point_list_line_string)
                trail.save()
                print(trail.title)
        print('done')
                    
