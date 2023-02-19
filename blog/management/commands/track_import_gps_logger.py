# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:10:24 2019

@author: mark
"""

from django.core.management.base import BaseCommand, CommandError
from blog.models import Picture, Post, Trail
from blog.helper.get_df import load_single_df_text_time_gpslogger
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point, LineString
import time, json, os, psycopg2, shutil
import datetime, time
import pandas as pd
from haversine import haversine


class Command(BaseCommand):
        
    
    def get_json_and_line_string(self, df):
        """
        Get a json string {'lat', 'lon', 'elevation', 'time'} from track file
        and return
        """
        point_list = []
        point_list_line_string = []
        total_distance = 0
        start_point = (float(df.loc[0, 'latitude']), 
                      float(df.loc[0, 'longitude']))
        for pt in range(0,len(df)):
            current_point = (float(df.loc[pt, 'latitude']), 
                             float(df.loc[pt, 'longitude']))
            
            p2p_distance = haversine(start_point, current_point, unit='mi')
            start_point = current_point
            total_distance = p2p_distance + total_distance
            insert_dict = {'time': df.loc[pt,'date time'],
                           'elevation':df.loc[pt, 'altitude(m)'],
                           'lat':df.loc[pt, 'latitude' ],
                            'lon':df.loc[pt, 'longitude'],
                           'p2p_distance':p2p_distance,
                           'total_distance': total_distance}
            point_list.append(insert_dict)
            point_list_line_string.append( (float(df.loc[pt, 'longitude']),
                                            float(df.loc[pt, 'latitude']) ) )
            
    
        json_str = json.dumps(point_list)
        print(total_distance)
        return json_str, point_list_line_string
    


    def handle(self, *args, **options):
        
        title = "Mt Massive"
        gpx_file = "/home/mark/Pictures/2022/August_Colorado/18/20220818-052917 - HikeMtMassive100log.txt"
        
        
        print(gpx_file[:-4])

        df = load_single_df_text_time_gpslogger(gpx_file)
        json_string, point_list = self.get_json_and_line_string(df)

        

        new_trail = Trail()
        new_trail.bing_json_track = json_string
        new_trail.title = title
        new_trail.url_title = title.lower().replace(' ','_')
        new_trail.line_string = LineString(point_list)
        new_trail.save()
        print(new_trail.id)
        print('run reduce_tracks and reduce_graph')
















