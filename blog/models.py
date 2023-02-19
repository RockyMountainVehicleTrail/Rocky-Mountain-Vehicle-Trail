from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Post(models.Model):
    desc = models.TextField(blank=True, null=True)


class Person(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class HistoricTrail(models.Model):
    title = models.TextField(blank=True, null=True)
    url_title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    multi_line_string = models.MultiLineStringField(blank=True, null=True)
    publish_to_web = models.BooleanField(default=False, blank=True, null=True)
    citation = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'No title'


class LewisAndClark(models.Model):
    FID = models.IntegerField()
    source = models.TextField(blank=True, null=True)
    exped_seg = models.TextField(blank=True, null=True)
    trip_type = models.TextField(blank=True, null=True)
    trail_type = models.TextField(blank=True, null=True)
    leader = models.TextField(blank=True, null=True)
    journey = models.TextField(blank=True, null=True)
    multi_line_string = models.MultiLineStringField(blank=True, null=True)
    
class LewisAndClarkPOI(models.Model):
    site_name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    street_add = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    site_type = models.TextField(blank=True, null=True)
    hphs = models.TextField(blank=True, null=True)
    unigrid = models.TextField(blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    
class LewisAndClarkCampsites(models.Model):
    label = models.TextField(blank=True, null=True)
    label2 = models.TextField(blank=True, null=True)
    camp_text = models.TextField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    
    
class LewisAndClarkPotentialSites(models.Model):
    name = models.TextField(blank=True, null=True)
    state  = models.TextField(blank=True, null=True)
    counties = models.TextField(blank=True, null=True)
    owntyp = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    lecl_url = models.URLField(blank=True, null=True)
    lecl_photo = models.URLField(blank=True, null=True)
    lecl_thumb = models.URLField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)




class Camera(models.Model):
    brand = models.TextField()
    
    def __str__(self):
        return self.brand
    

class Category(models.Model):
    description = models.TextField()
    
    
class HistoricTrailPoint(models.Model):
    description = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    point = models.PointField()
    person = models.ManyToManyField(Person, blank=True)
    historic_trail = models.ForeignKey(HistoricTrail, blank=True, null=True, on_delete=models.PROTECT)
    audio_file = models.FileField(upload_to='historic_point_audio', blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    


class Trail(models.Model):
    """
    Hiking trails.  mostly from recording tracks I went one,
    but some are from the the national map transportation  dataset
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    raw_track = models.TextField(blank=True, null=True)
    bing_json_track = models.TextField(blank=True, null=True)
    reduced_json_track = models.TextField(blank=True, null=True)
    line_string = models.LineStringField(blank=True, null=True)
    reduced_line_string = models.LineStringField(blank=True, null=True)
    web_line_string = models.LineStringField(blank=True, null=True)
 
    def __str__(self):
        if self.title:
            return '{} -- {}'.format(self.title, self.url_title)
        else:
            return 'No title'


class ScenicDrive(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=100, blank=True, null=True)
    multi_line_string = models.MultiLineStringField(blank=True, null=True)
    reduced_multi_line_string = models.MultiLineStringField(blank=True, null=True)
    official = models.BooleanField(default=True, blank=True, null=True)
#    ranking = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'No title'



class State(models.Model):
    """
    From Natural Earth data.  The big polygons took to long to load
    so I made smaller ones in reduced mulit polygon
    """
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_lower = models.CharField(max_length=100, blank=True, null=True)
    type_en  = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=100, blank=True, null=True)
    admin = models.CharField(max_length=100, blank=True, null=True)
    adm0_a3 = models.CharField(max_length=100, blank=True, null=True)                        
    multi_polygon = models.MultiPolygonField(blank=True, null=True)
    reduced_multi_polygon = models.MultiPolygonField(blank=True, null=True)
    
    def __str__(self):
        return('{}---{}--{}--{}'.format(self.name_en, self.admin, self.adm0_a3, self.name_lower))


                             
                             
class ScenicDriveIndividualLineString(models.Model):
    """
    I don't think it's used any more
    Individual line string for each scenic drive.  Since they may be made
    up of segments with different highways it makes sense be able to break the 
    information down.
    Fields match census roads columns.  Since I do not know the variety of data type
    everything is a charfield"""
    linearid = models.CharField(max_length=50, blank=True, null=True)
    fullname = models.CharField(max_length=50, blank=True, null=True)
    rttyp = models.CharField(max_length=50, blank=True, null=True)
    mtfcc = models.CharField(max_length=50, blank=True, null=True)
    line_string = models.LineStringField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    scenic_drive = models.ForeignKey(ScenicDrive, blank=True, null=True, on_delete=models.SET_NULL)
    
    
class Picture(models.Model):
    lat = models.CharField(max_length=10, blank=True, null=True)
    lon = models.CharField(max_length=10, blank=True, null=True)
    lat_ref= models.CharField(max_length=10, blank=True, null=True)
    lon_ref = models.CharField(max_length=10, blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    image_datetime = models.DateTimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    picture = models.FileField(upload_to='media')
    small_picture = models.ImageField(upload_to='small_media', blank=True, null=True)
    labeled_picture = models.ImageField(upload_to='label_media', blank=True, null=True)
    label = models.CharField(max_length=3, blank=True, null=True)
    trail = models.ForeignKey(Trail, blank=True, null=True, on_delete=models.SET_NULL)
    point = models.PointField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    camera = models.ForeignKey(Camera, blank=True, null=True, on_delete=models.SET_NULL)
    f_number = models.CharField(blank=True, null=True, max_length=15)
    focal_length = models.CharField(blank=True, null=True, max_length=15)
    exposure_time = models.CharField(blank=True, null=True, max_length=15)
    iso = models.CharField(blank=True, null=True, max_length=15)
    original_filename = models.CharField(blank=True, null=True, max_length=55)
    

class Place(models.Model):
    """
    Intent was to make travel planning for place like Yellowstone etc.
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    multi_polygon = models.MultiPolygonField(blank=True, null=True)
    reduced_multi_polygon = models.MultiPolygonField(blank=True, null=True)
    admin_unit_name = models.CharField(max_length=100, blank=True, null=True)
    admin = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'No title'
        
        
        
class PointOfInterest(models.Model):
    point = models.PointField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    basename = models.CharField(max_length=100, blank=True, null=True)
    

    
class Feature(models.Model):
    """
    Features from The National Map features and some from Canadian sources
    """
    description = models.TextField(blank=True, null=True)
    point = models.PointField()
    feature_name = models.CharField(max_length=100, blank=True, null=True)
    feature_class = models.CharField(max_length=100, blank=True, null=True)
    state_alpha = models.CharField(max_length=100, blank=True, null=True)
    county_name = models.CharField(max_length=100, blank=True, null=True)
    elev_in_ft = models.CharField(max_length=100, blank=True, null=True)
    map_name = models.CharField(max_length=100, blank=True, null=True)
    geoname = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    prov_terr  = models.CharField(max_length=100, blank=True, null=True)
    generic = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        if self.elev_in_ft == None:
            return str(self.geoname)
        if self.feature_name:
            return str(self.feature_name)
        elif self.map_name:
            return str(self.map_name)
        else:
            return 'No Name'
            
    def get_name(self):
        if self.elev_in_ft == None:
            return self.geoname
        else:
            return self.feature_name


class IndianLand(models.Model):
    """
    Taken from a BIA o BLM dataset that has most of the treaties that were
    made with various tribes
    """
    OBJECTID = models.IntegerField(blank=True, null=True)
    CESSNUM = models.CharField(max_length=5, blank=True, null=True)
    CESSNUMSORT = models.IntegerField(blank=True, null=True)
    MAPNAME = models.CharField(max_length=255, blank=True, null=True)
    STATE = models.CharField(max_length=50, blank=True, null=True)
    COUNTY = models.CharField(max_length=1500, blank=True, null=True)
    STATECOUNTY = models.CharField(max_length=2000, blank=True, null=True)
    SCHDTRB = models.CharField(max_length=255, blank=True, null=True)
    PRESDAYTRB = models.CharField(max_length=2000, blank=True, null=True)
    CITATION1 = models.CharField(max_length=500, blank=True, null=True)
    CITATION2 = models.CharField(max_length=500, blank=True, null=True)
    CESSDATE1 = models.DateTimeField(blank=True, null=True)
    DATE1LINK_ROYCE_SCHEDULE = models.CharField(max_length=255, blank=True, null=True)
    DATE1LINK_KAPPLER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    CESSDATE2 = models.DateTimeField(blank=True, null=True)
    DATE2LINK_ROYCE_SCHEDULE = models.CharField(max_length=255, blank=True, null=True)
    DATE2LINK_KAPPLER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    CESSDATE3 = models.DateTimeField(blank=True, null=True)
    DATE3LINK_ROYCE_SCHEDULE = models.CharField(max_length=255, blank=True, null=True)
    DATE3LINK_KAPPLER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    CESSDATE4 = models.DateTimeField(blank=True, null=True)
    DATE4LINK_ROYCE_SCHEDULE = models.CharField(max_length=255, blank=True, null=True)
    DATE4LINK_KAPPLER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    CESSDATE5 = models.DateTimeField(blank=True, null=True)
    DATE5LINK_ROYCE_SCHEDULE = models.CharField(max_length=255, blank=True, null=True)
    DATE5LINK_KAPPLER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME1 = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME2 = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME3 = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME4 = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME5 = models.CharField(max_length=255, blank=True, null=True)
    MAPNAME6 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL1 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL2 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL3 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL4 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL5 = models.CharField(max_length=255, blank=True, null=True)
    MAPURL6 = models.CharField(max_length=255, blank=True, null=True)
    LINK_FEDERAL_STATUTE = models.CharField(max_length=255, blank=True, null=True)
    LINK_EXECUTIVE_ORDER = models.CharField(max_length=255, blank=True, null=True)
    LINK_OTHER_TREATY = models.CharField(max_length=255, blank=True, null=True)
    multi_polygon = models.MultiPolygonField(blank=True, null=True)
    annual_report_text = models.TextField(blank=True, null=True)
    annual_report_historic_remarks = models.TextField(blank=True, null=True)
    publish_to_web = models.BooleanField(default=False)


    def __str__(self):
        if self.CESSNUM:
            return self.CESSNUM
        else:
            return 'Nada'


class SpanishEngWord(models.Model):
    word = models.CharField(max_length=24, blank=True, null=True)
    pos = models.CharField(max_length=24, blank=True, null=True)
    spanish_phrase = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.word


class SpanishWord(models.Model):
    word = models.CharField(max_length=24, blank=True, null=True)
    pos = models.CharField(max_length=24, blank=True, null=True)
    pos_sub = models.CharField(max_length=24, blank=True, null=True)
    gender = models.CharField(max_length=24, blank=True, null=True)
    eng_trans = models.TextField(blank=True, null=True)
    appleton = models.TextField(blank=True, null=True)
    special = models.BooleanField(default=False)
    special_num = models.CharField(max_length=24, blank=True, null=True)
    special_sub = models.CharField(max_length=24, blank=True, null=True)
    morphed = models.BooleanField(default=False)
    
    def __str__(self):
        return '{}'.format(self.word)
        
    
class SpanishMorph(models.Model):
    form  = models.CharField(max_length=100, blank=True, null=True)
    lower_form  = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    def_id = models.ForeignKey('SpanishWord', blank=True, null=True, on_delete=models.SET_NULL)
    pos = models.CharField(max_length=24, blank=True, null=True)
    pos_sub = models.CharField(max_length=24, blank=True, null=True)
    pos_group = models.CharField(max_length=6, blank=True, null=True)
    gender = models.CharField(max_length=24, blank=True, null=True)
    concat  = models.TextField(blank=True, null=True)
    person  = models.CharField(max_length=30, blank=True, null=True)
    number  = models.CharField(max_length=30, blank=True, null=True)
    tense  = models.CharField(max_length=30, blank=True, null=True)
    mood  = models.CharField(max_length=30, blank=True, null=True)
    voice  = models.CharField(max_length=30, blank=True, null=True)        
    extra  = models.CharField(max_length=30, blank=True, null=True)


class LanguagePage(models.Model):
    title = models.TextField()
    url_title = models.TextField(blank=True, null=True)
    video_url = models.TextField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    language = models.CharField(blank=True, null=True, max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class LanguagePageLine(models.Model):
    language_page = models.ForeignKey(LanguagePage, on_delete=models.PROTECT)
    picture = models.ForeignKey(Picture, blank=True, null=True, on_delete=models.PROTECT)
    chapter = models.IntegerField(blank=True, null=True)
    line_num = models.IntegerField()
    english = models.TextField(blank=True, null=True)
    spanish = models.TextField(blank=True, null=True)
    german = models.TextField(blank=True, null=True)
    latin = models.TextField(blank=True, null=True)


class WhitFull(models.Model):
    """
    Contains the actual words with defintions.        
    Created the dictionary from whitakers words different from pslaterdict
    since that way I can remove on or the other."""
    word = models.CharField(max_length=24, blank=True, null=True)
    pos = models.CharField(max_length=24, blank=True, null=True)
    pos_sub = models.CharField(max_length=24, blank=True, null=True)
    pos_group = models.CharField(max_length=6, blank=True, null=True)
    gender = models.CharField(max_length=24, blank=True, null=True)
    genitive_stem  = models.CharField(max_length=24, blank=True, null=True)
    present_stem  = models.CharField(max_length=24, blank=True, null=True,
                                     help_text='Masculine ADJ.')
    perfect_stem  = models.CharField(max_length=24, blank=True, null=True,
                                     help_text='Fem ADJ.')
    supine_stem  = models.CharField(max_length=24, blank=True, null=True,
                                    help_text='Neut ADJ.')
    alt_perfect_stem  = models.CharField(max_length=24, blank=True, null=True)
    alt_supine_stem  = models.CharField(max_length=24, blank=True, null=True)
    comparative = models.CharField(max_length=24, blank=True, null=True)
    superlative = models.CharField(max_length=24, blank=True, null=True)
    endings = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    reviewed = models.IntegerField(default=0)
    source = models.CharField(max_length=10, blank=True, null=True)
    o_word = models.CharField(max_length=24, blank=True, null=True,
                              help_text='Original word from Whitaker')

    def __str__(self):
        return self.word
    

class WhitMorphFull(models.Model):
    """built from Whitakers Words and tables I made to provide known forms of words.
    the goal is to go through the Bible verse by verse cleaning all the entries"""
    form  = models.CharField(max_length=30, blank=True, null=True)
    lower_form  = models.CharField(db_index=True, max_length=30, blank=True, null=True)

    pos  = models.CharField(max_length=30, blank=True, null=True)
    pos_sub  = models.CharField(max_length=30, blank=True, null=True)
    gender  = models.CharField(max_length=30, blank=True, null=True)
    wcase  = models.CharField(max_length=30, blank=True, null=True)
    pos_group  = models.CharField(max_length=30, blank=True, null=True)

    person  = models.CharField(max_length=30, blank=True, null=True)
    number  = models.CharField(max_length=30, blank=True, null=True)
    tense  = models.CharField(max_length=30, blank=True, null=True)
    mood  = models.CharField(max_length=30, blank=True, null=True)
    voice  = models.CharField(max_length=30, blank=True, null=True)
    comparative  = models.CharField(max_length=30, blank=True, null=True)
    verb_sub  = models.CharField(max_length=30, blank=True, null=True)
    verb_sub_pos  = models.CharField(max_length=30, blank=True, null=True)
    ver_sub_group  = models.CharField(max_length=30, blank=True, null=True)
    display_pos = models.IntegerField(blank=True, null=True)

    concat  = models.TextField(blank=True, null=True)

    def_id = models.ForeignKey('WhitFull', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{}: {}'.format(self.def_id.word, self.concat)
        
