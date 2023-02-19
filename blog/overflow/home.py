# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:48:06 2019
https://blackrockdigital.github.io/startbootstrap-simple-sidebar/
@author: mark
"""

from blog.models import (Picture, Post, Trail, ScenicDrive, 
                         State, Feature,
                     HistoricTrail, HistoricTrailPoint, Person, Place)
from django.contrib.gis.geos import Point, LineString
from django.shortcuts import render
from django.contrib.gis.measure import D, Distance


def terms_conditions(request):
    return render(request, 'terms_conditions.html')
    
def terms_privacy(request):
    return render(request, 'terms_privacy.html')
    
def terms_cookies(request):
    return render(request, 'terms_cookies.html')

def terms_about(request):
    return render(request, 'terms_about.html')
    
def hiking_tutorial(request):
    return render(request, 'hiking_tutorial.html')

def home(request):
    states = State.objects.all()
    
    context = {
        'states': states,        
        }

    return render(request, 'home.html', context)
    


def places_home(request):
    states = State.objects.all()
    places = Place.objects.all()
    
    context = {
        'states': states,
        'places':places,    
    }
    
    return render(request, 'places_home.html', context)
    

def things_to_do_place(request, place_name):
    states = State.objects.all()

    place_qry = Place.objects.filter(url_title=place_name)
    if place_qry:
        place = place_qry[0]
        features = Feature.objects.filter(point__within=place.multi_polygon)
        drives = ScenicDrive.objects.filter(multi_line_string__bboverlaps=place.multi_polygon)
        trails = Trail.objects.filter(reduced_line_string__bboverlaps=place.multi_polygon)
        pics = Picture.objects.filter(point__within=place.multi_polygon)
    print('feature_count = {}'.format(len(features)))
    context = {
        'states': states,
#        'state':state_name,
        'features':features,
        'drives':drives,
        'place':place,
        'trails':trails,
        'pics':pics,
        }
        
    print('len trails {}'.format(trails.count()))
    
    return render(request, 'things_to_do_place.html', context)

    
    

def sd_home(request):
    states = State.objects.all()    
    context = {
        'states': states,        
        }
        
    return render(request, 'sd_home.html', context)
    
    
    
def hike_home(request):
    states = State.objects.all()
    context = {
        'states': states,        
        }

    return render(request, 'hike_home.html', context)
    
    


def scenic_drives_state(request, state_name):
    states = State.objects.all()

    state_qry = State.objects.filter(name_lower=state_name)
    if state_qry:
        state = state_qry[0]
        features = Feature.objects.filter(point__within=state.multi_polygon)
        drives = ScenicDrive.objects.filter(multi_line_string__bboverlaps=state.multi_polygon)
        trails = Trail.objects.filter(reduced_line_string__bboverlaps=state.multi_polygon)
    print('feature_count = {}'.format(len(features)))
    context = {
        'states': states,        

#        'state':state_name,
        'features':features,
        'drives':drives,
        'state':state,
        'trails':trails,
        }
        
    return render(request, 'scenic_drives_state.html', context)
    
 
def hikes_drives_state(request, state_name):
    states = State.objects.all()

    state_qry = State.objects.filter(name_lower=state_name)
    if state_qry:
        state = state_qry[0]
        features = Feature.objects.filter(point__within=state.multi_polygon)
        drives = ScenicDrive.objects.filter(multi_line_string__bboverlaps=state.multi_polygon)
        trails = Trail.objects.filter(reduced_line_string__bboverlaps=state.multi_polygon)
    print('feature_count = {}'.format(len(features)))
    print(state.admin)
    context = {
        'states':states,
        'features':features,
        'drives':drives,
        'state':state,
        'trails':trails,
        }
        
    print('len trails {}'.format(trails.count()))
    
    return render(request, 'hikes_drives_state.html', context)

   
    
def best_hikes_state(request, state_name):
    states = State.objects.all()
    state_qry = State.objects.filter(name_lower=state_name)
    if state_qry:
        state = state_qry[0]
        trails = Trail.objects.filter(reduced_line_string__bboverlaps=state.multi_polygon) 
        print('trails {}'.format(len(trails)))
        
    context = {
        'states': states,        
        'trails':trails,
        'state':state
        }  
    return render(request, 'best_hikes_state.html', context)
    
    
    
def trail_name(request, trail_name):
    states = State.objects.all()
    print('states')
    trail = Trail.objects.get(url_title=trail_name)
    lstr = trail.line_string
    lstr = trail.reduced_line_string
    print('line string')
    trail_buffer = lstr.buffer(.001)
    print('buffer')
#    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=25)))
    pics = Picture.objects.filter(point__bboverlaps=trail_buffer)
    print('after_pics')
    state_qry = State.objects.filter(multi_polygon__contains=trail.line_string)
    if state_qry.count() == 0:
        state = State.objects.get(name_en='Alberta')
    else:
        state = state_qry[0]    
    print(trail)
    context = {
        'states': states,        

        'state':state,
        'trail':trail,
        'pics': pics
        }

    return render(request, 'hike_name_markers.html', context)
    
    
def scenic_drive_name(request, sd_name):
    states = State.objects.all()

    scenic_drive_qry = ScenicDrive.objects.filter(url_title=sd_name)
    if scenic_drive_qry:
        
        scenic_drive = scenic_drive_qry[0]
        state_qry = State.objects.filter(multi_polygon__contains=scenic_drive.multi_line_string)
        print('COunt {}'.format(state_qry.count()))
        if state_qry.count() == 0: # requires a different basemap etc.
            state = State.objects.get(name_en='Alberta')
        else:
            state = state_qry[0]
    
        sd_buffer = scenic_drive.multi_line_string.buffer(.001)
        feature_buffer = scenic_drive.multi_line_string.buffer(.01)
        pics = Picture.objects.filter(point__bboverlaps=sd_buffer)
        features = Feature.objects.filter(point__bboverlaps=feature_buffer)
        # for pic in pics:
        #     print(pic.id)
    context = {
        'states': states,        

        'state':state,
        'scenic_drive':scenic_drive,
        'pics':pics,
        'features':features
        }

    return render(request, 'scenic_drive_name.html', context)    
    
    
def language_learning(request):
    return render(request, 'language_learning.html')
    
    


    
    
    
    