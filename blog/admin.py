from django.contrib import admin
from django.contrib.gis import admin

# Register your models here.


from .models import (Picture, Post, Trail, ScenicDrive, PointOfInterest, 
                     ScenicDriveIndividualLineString, State,
                     HistoricTrail, HistoricTrailPoint, Person, Camera,
                     Feature, Place, IndianLand, SpanishEngWord, SpanishWord,
                     SpanishMorph, LanguagePage, LanguagePageLine,
                     WhitFull, WhitMorphFull, LewisAndClarkPotentialSites)

admin.site.register(WhitFull)
admin.site.register(WhitMorphFull)
admin.site.register(LewisAndClarkPotentialSites)
admin.site.register(LanguagePage)
admin.site.register(SpanishMorph)
admin.site.register(Post)
admin.site.register(Place)
admin.site.register(PointOfInterest)
admin.site.register(HistoricTrail)
admin.site.register(HistoricTrailPoint)
admin.site.register(Person)
admin.site.register(Camera)
admin.site.register(State)
admin.site.register(IndianLand)
admin.site.register(ScenicDriveIndividualLineString)
admin.site.register(ScenicDrive)


@admin.register(LanguagePageLine)
class LanguagePageLine(admin.ModelAdmin):
    fields = ['chapter', 'line_num', 'english', 'spanish']
    list_display = ['chapter', 'line_num', 'english', 'spanish', 'german']
#    list_editable = [ 'english']
    list_filter = ['chapter', 'language_page']


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    fields = ('title', 'url_title', 'description', 'rating')
    list_display = ['title', 'url_title', 'description', 'rating']
    list_filter = ['title', 'url_title', 'description', 'rating']

admin.site.register(Feature)


@admin.register(SpanishWord)
class SpanishWordAdmin(admin.ModelAdmin):
    fields = ( 'word', 'pos', 'eng_trans', 'appleton', 'special_num', 'gender')
    list_display = ('word', 'pos', 'eng_trans', 'appleton', 'special_num', 'gender')
    list_filter = ('pos', 'special_num')
    list_search = ('word','eng_trans' )
    search_fields = ['word', 'eng_trans']
    

@admin.register(SpanishEngWord)
class SpanishEngWordAdmin(admin.ModelAdmin):
    fields = ( 'word', 'pos', 'spanish_phrase')
    list_display = ('word', 'pos', 'spanish_phrase')
    list_filter = ('pos', )
    list_search = ('spanish_phrase', )
    search_fields = ['word']


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    
    fields = ('image_datetime', 'date', 'time', 'camera', 'original_filename',
              'point', 'small_picture', 'picture')
    list_display = ('image_datetime', 'date', 'time', 'camera', 'original_filename')
    list_filter = ['camera']
    
