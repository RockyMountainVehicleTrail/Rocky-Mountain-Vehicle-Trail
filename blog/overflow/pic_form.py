# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:30:01 2019

@author: mark
Display all pictures with location data on the map.  I rarely use the option to
rotate or add description, but some of these were useful for the initial
load.  The delete is also somewhat obsolete, as I modified the javascript to
add the pictures I want to delete to an array, then I use the developers
console to copy the ids and use the management command delete_by_ids to remove
the pictures.  It is much quicker.
"""

from blog.models import Picture
from django.shortcuts import render
from wand.image import Image
from blog.forms import PictureForm
from django.views import View

class PicFormView(View):
    
    form_class = PictureForm    
    
    def get(self, request):
#        pics = Picture.objects.all()
        pics = Picture.objects.filter(point__isnull=False)
        form = PictureForm
        context = {
            'pics':pics,
            'form':form,
            'lon':-108.3830,
            'lat':44.842777,
            'zoom':10
            
            }
        print(pics.count())

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
                    
        pics = Picture.objects.filter(point__isnull=False)

        form = PictureForm
        context = {
            'pics':pics,
            'form':form,
            'lon':lon,
            'lat':lat,
            'zoom':zoom
            }
        print(pics.count())
        return render(request, 'pics_form.html', context)  
        






        