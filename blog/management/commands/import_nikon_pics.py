# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:32:47 2019

@author: mark
Imports pictures from Nikon
"""
from django.core.management.base import BaseCommand, CommandError
from blog.models import Picture, Post, Camera
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point
import re, pickle, json, os, psycopg2, shutil
import datetime, time
import datetime as datetime_main
from datetime import timedelta
from datetime import datetime
from pytz import timezone
from tzwhere import tzwhere
import pandas as pd

import exifread
from wand.image import Image



import tempfile

import numpy as np


class Command(BaseCommand):
    """ August 12th not imported"""
#    BASE_PATH = '/media/mark/testvol2/2019/December/28/'
    BASE_PATH = '/media/mark/testvol2/2020/August/14/'
    
    def load_merged_df(self, base_path):
        """
        Merged all csv tracks into one df and return
        """
        file_list = os.listdir(base_path)
        df_list = []
        for csv_file in file_list:
            if csv_file[-4:] == '.csv':
                print(csv_file[-4:])
                temp_df = pd.read_csv(os.path.join(base_path, csv_file), header=2)
                temp_df['Time'] = temp_df['Time'].astype('datetime64[ns]')
                df_list.append(temp_df)
        print(len(df_list))
        merged_df = pd.concat(df_list)
        sorted_df = merged_df.sort_values('Time')
   
        return sorted_df

    def get_timezone(self, df):
        lat = df.iloc[0]['Latitude (deg)']
        lon = df.iloc[0]['Longitude (deg)']
        tzw = tzwhere.tzwhere()
        return tzw.tzNameAt(lat,lon)   
        
        
    def handle(self, *args, **options):
        
        df = self.load_merged_df(self.BASE_PATH)
        time_zone = self.get_timezone(df)
        dir_list = os.listdir(self.BASE_PATH)
        cam = 'Nikon'
        cam_model = Camera.objects.get(brand='Nikon')
        file_list = os.listdir(os.path.join(self.BASE_PATH, cam, 'web'))
        pic_list = []
        for f in file_list:
            if f[-4:] == '.JPG':
                pic_list.append(f)
        pic_list.sort()
        for pic_file in pic_list:
            with open(os.path.join(self.BASE_PATH, cam, pic_file), 'rb') as infile:
                tags = exifread.process_file(infile)
                print('{}\t{}'.format(pic_file, tags['EXIF DateTimeOriginal']))
                idatetime = tags['Image DateTime']
                idatetime = tags['EXIF DateTimeOriginal']
                pic_dt = datetime.strptime(idatetime.values, '%Y:%m:%d %H:%M:%S')
                tz_localizer = timezone(time_zone)
                local_pic_dt = tz_localizer.localize(pic_dt)
                date_time_series = df['Time']
                position = date_time_series.searchsorted(np.datetime64(local_pic_dt))
                if position >= len(df):
                    position = position - 1

                long = df.iloc[position]['Longitude (deg)']
                lat = df.iloc[position]['Latitude (deg)']
                
                new_pic = Picture()
                new_pic.camera = cam_model
                new_pic.picture.save(pic_file, infile)    
                print('ID:{}\tTime: {}\tPos: {} \n{},{}'.format(
                        new_pic.id, idatetime, position,
                        df.iloc[position]['Latitude (deg)'],
                        df.iloc[position]['Longitude (deg)']
                    ))
                new_pic.lat = str(lat)[0:9]
                new_pic.lon = str(long)[0:9]
                new_pic.point = Point(long,lat)
                if 'EXIF DateTimeOriginal' in tags.keys():
                    t = tags['EXIF DateTimeOriginal'].values.replace(' ', ':').split(':')
                    dt_insert = datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]))
                    new_pic.image_datetime = dt_insert
                new_pic.elevation = df.iloc[position]['Altitude (m)']
                new_pic.date = new_pic.image_datetime.date()
                
                if 'EXIF FNumber' in tags.keys():
                    new_pic.f_number = tags['EXIF FNumber'].printable
                    
                if 'EXIF FocalLength' in tags.keys():
                    new_pic.focal_length = tags['EXIF FocalLength'].printable
                
                if 'EXIF ISOSpeedRatings' in tags.keys():
                    new_pic.iso = tags['EXIF ISOSpeedRatings'].printable
                    
                if 'EXIF ExposureTime' in tags.keys():
                    new_pic.exposure_time = tags['EXIF ExposureTime'].printable
                
                new_pic.original_filename = pic_file
                w1 = Image(filename=os.path.join(self.BASE_PATH, cam, pic_file))
                small_temp_file = tempfile.TemporaryFile()
                w1.resize(int(w1.size[0]*.15), int(w1.size[1]*.15))
                w1.save(small_temp_file)
                new_pic.small_picture.save('small_label.jpg', small_temp_file)
                new_pic.save()
                print(new_pic.id)

