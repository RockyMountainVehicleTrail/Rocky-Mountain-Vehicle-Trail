# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:32:47 2019

@author: mark
Works with pic_form see comments there.
"""
from django.core.management.base import BaseCommand, CommandError
from blog.models import Picture, Post
from django.core.files import File
from django.conf import settings



class Command(BaseCommand):
    

    def handle(self, *args, **options):
#        print('hello there uncomment to run')
#        with open('/home/mark/Projects/hiking/scratch/ids_to_remove.txt') as infile:
#            file_lines = infile.readlines()
        with open('/home/mark/Projects/hiking/scratch/pics_to_delete/delete.txt', 'w') as ofile:
            file_lines =  ['9628', '9690', '9687', '9666', '9651', '9725', '9713', '9709', '9701']
            for pid in file_lines:
                pk_id = pid.strip()
                if len(pk_id) < 2:
                    print('none')
                else:
                    ofile.write('\n\n{}\n'.format(pid))
                    pics = Picture.objects.filter(pk=pk_id)
                    if len(pics) == 1:
                        cpic = pics[0]
                        if cpic.small_picture.name:
                            cpic.small_picture.delete()
                            ofile.write('small\t{}'.format(cpic.small_picture.name))
                        if cpic.picture.name:
                            ofile.write('reg\t{}'.format(cpic.picture.name))
                            cpic.picture.delete()
                        if cpic.labeled_picture.name:
                            ofile.write('label\t{}'.format(cpic.labeled_picture.name))
                            cpic.labeled_picture.delete()
                        cpic.delete()
                    ofile.write('\n\n')
            print('done')

























