# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:12:25 2020

@author: mark
"""
from django.contrib.gis.geos import GEOSGeometry
from blog.models import (Picture, Trail, ScenicDrive, Feature,
                         HistoricTrail, HistoricTrailPoint, State, IndianLand,
                         LewisAndClark, LewisAndClarkPOI, LewisAndClarkCampsites,
                         LewisAndClarkPotentialSites)
from django.contrib.gis.geos import Point, LineString
from django.shortcuts import render
from django.contrib.gis.measure import D, Distance



def history_main(request):
    return render(request, 'the_vacation_historian.html')



def historic_trails_all(request):
    states = State.objects.all()

    hist_trails = HistoricTrail.objects.filter(publish_to_web=True)
    
    context = {
        'states': states,        
        'hist_trails':hist_trails
    }
    
    return render(request, 'historic_trails_all.html', context)
    
    
    
def historic_trail_name(request, trail_name):
    trail_qry = HistoricTrail.objects.filter(url_title=trail_name)
    trail = trail_qry[0]
    trail_points = HistoricTrailPoint.objects.filter(historic_trail=trail)
    states = State.objects.all()
    trail_buffer = trail.multi_line_string.buffer(.1)
    pics = Picture.objects.filter(point__within=trail_buffer)
    features = Feature.objects.filter(point__within=trail_buffer)

    
    context = {
        'trail':trail,
        'trail_points':trail_points,
        'states': states,
        'features':features,
        'pics':pics,

    }
    
    return render(request, 'historic_trail_name.html', context)
    

def lewis_and_clark(request):
    states = State.objects.all()
    trail = LewisAndClark.objects.all()
    lc_pois = LewisAndClarkPOI.objects.all()
    lc_camps = LewisAndClarkCampsites.objects.all()
    lc_pot_sites = LewisAndClarkPotentialSites.objects.all()
#    print(ceded_lands.count())
    
    context = {
        'states':states,    
        'trail':trail,
        'lc_pois':lc_pois,
        'lc_camps':lc_camps,
        'lc_pot_sites': lc_pot_sites
            }
    
    return render(request, 'lewis_and_clark.html', context)
    
    
    
def tribal_ceded_lands(request):
    states = State.objects.all()
    ceded_lands = IndianLand.objects.filter(publish_to_web=True)
    print(ceded_lands.count())
    
    context = {
        'states':states,    
        'ceded_lands':ceded_lands
            }
    
    return render(request, 'tribal_ceded_lands.html', context)


def tribal_ceded_land_cessnum(request, req_cessnum):
    states = State.objects.all()
    ceded_land = IndianLand.objects.get(CESSNUM=req_cessnum)
    print(ceded_land)
    
    context = {
        'states':states,    
        'ceded_land':ceded_land
            }
    
    return render(request, 'tribal_ceded_land_cessnum.html', context)








