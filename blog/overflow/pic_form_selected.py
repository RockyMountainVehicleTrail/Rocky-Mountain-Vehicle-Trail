# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:30:01 2019
all file not used
@author: mark
"""
from blog.models import Picture, Post
from django.shortcuts import render
from wand.image import Image
import datetime

from blog.forms import PictureForm
from django.views import View

class PicFormSelectedView(View):
  
    
    form_class = PictureForm    
    
    def get_query(self):
        camera = 'Nikon'
        edit_date = datetime.date(2019, 7, 15)        
        
        pics = Picture.objects.filter(date=edit_date)
        pics = pics.filter(camera__brand=camera)
#        pics = Picture.objects.filter(camera__brand=camera)
        return pics
    
    def get(self, request):
        
        
        
        pics = self.get_query()
        form = PictureForm
        if pics.count() > 0:
            lon = pics[0].point.x
            lat = pics[0].point.y
        else:
            lon = -108.3830
            lat = 44.84277
        context = {
            'pics':pics,
            'form':form,
            'lon':lon,
            'lat':lat,
            'zoom':10
            
            }
    
        return render(request, 'pics_form.html', context)  
        
        
    def post(self, request):
        
#        print(request.POST)
        pic_form = PictureForm(request.POST)
        lon = -108.3830
        lat = 44.842777
        zoom = 4
        if pic_form.is_valid():
            print('pic_form', pic_form.cleaned_data)
            cpk = pic_form.cleaned_data['pic_id']
            cpic_qry = Picture.objects.filter(pk=cpk)
            if cpic_qry.count() == 1:
                cpic = cpic_qry[0]
                print('1')
                lon = cpic.lon
                lat = cpic.lat
                zoom = 16
                if pic_form.cleaned_data['delete'] == True:
                    if cpic.small_picture.name:
                        cpic.small_picture.delete()
                    if cpic.picture.name:
                        cpic.picture.delete()
                    if cpic.labeled_picture.name:
                        cpic.labeled_picture.delete()
                    cpic.delete()
                else:
                    print(pic_form.cleaned_data['description'])
                    cpic.description = pic_form.cleaned_data['description']
                    cpic.save()
                    rotate_deg = pic_form.cleaned_data['rotate']
                    print(rotate_deg)
                    if rotate_deg != '0':
                        if cpic.small_picture.name:
                            if cpic.small_picture.name != '':
                                print(cpic.small_picture.file.name)
                                im = Image(filename=cpic.small_picture.file.name)
                                im.rotate(int(rotate_deg))
                                im.save(filename=cpic.small_picture.file.name)
                        if cpic.picture.name:
                            if cpic.picture.name != '':
                                print(cpic.picture.file.name)
                                im = Image(filename=cpic.picture.file.name)
                                im.rotate(int(rotate_deg))
                                im.save(filename=cpic.picture.file.name)
                    
            
            
        pics = self.get_query()
        form = PictureForm
        context = {
            'pics':pics,
            'form':form,
            'lon':lon,
            'lat':lat,
            'zoom':zoom
            }
    
        return render(request, 'pics_form_selected.html', context)  
        






        