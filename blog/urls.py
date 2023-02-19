# from django.conf.urls import url
from django.urls import re_path, include
from django.conf.urls.static import static
from django.conf import settings


from .overflow.pic_form import PicFormView
from .overflow.home import (home, scenic_drives_state, best_hikes_state,
                            trail_name, scenic_drive_name, sd_home, hike_home,
                            hikes_drives_state, language_learning, places_home,
                            things_to_do_place, hiking_tutorial,
                            terms_about, terms_privacy, terms_cookies, terms_conditions)
                            
from .overflow.language import (spanish_page, spanish_main, ingles_main, ingles_page)
from .overflow.verb_game import (verb_game, verb_game_main)
from .overflow.latin import (latin_page, latin_main)
from .overflow.historic import (history_main, historic_trails_all, historic_trail_name,
                                tribal_ceded_lands, tribal_ceded_land_cessnum,
                                lewis_and_clark)
                               

urlpatterns = [
    re_path(r'^home.html', home, name='home'),
    re_path(r'^sd_home.html', sd_home, name='sd_home'),
    re_path(r'^hike_home.html', hike_home, name='hike_home'),
    re_path(r'^places_home.html', places_home, name='places_home'),
    re_path(r'^things_to_do_([A-Za-z_]{1,60}).html$', things_to_do_place, name='things_to_do_place'),
    re_path(r'^scenic_drives_([A-Za-z_]{1,60}).html$', scenic_drives_state, name='scenic_drives_state'),
    re_path(r'^best_hikes_([A-Za-z_]{1,60}).html$', best_hikes_state, name='best_hikes_state'),
    re_path(r'^hikes_drives_([A-Za-z_]{1,60}).html$', hikes_drives_state, name='hikes_drives_state'),
    re_path(r'^trail_([A-Za-z_0-9]{1,60}).html$', trail_name, name='trail_name'),
    re_path(r'^sd_([A-Za-z_0-9]{1,60}).html$', scenic_drive_name, name='scenic_drive_name'),
    
    re_path(r'terms_about.html', terms_about, name='terms_about'),
    re_path(r'terms_conditions.html', terms_conditions, name='terms_conditions'),
    re_path(r'terms_privacy.html', terms_privacy, name='terms_privacy'),
    re_path(r'terms_cookies.html', terms_cookies, name='terms_cookies'),
    re_path(r'hiking_tutorial.html', hiking_tutorial, name='hiking_tutorial'),
    
    re_path(r'historic_trails', historic_trails_all, name='historic_trails_all'),
    re_path(r'the_vacation_historian.html', history_main, name='history_main'),
    re_path(r'historical_trails_all.html', historic_trails_all, name='historic_trails_all'),
    re_path(r'historic_trail_([A-Za-z_0-9]{1,60}).html$', historic_trail_name, name='historic_trail_name'),
    re_path(r'tribal_ceded_lands.html$', tribal_ceded_lands, name='tribal_ceded_lands'),
    re_path(r'tribal_ceded_land_cessnum_([0-9a]{2,5}).html$', tribal_ceded_land_cessnum, name='tribal_ceded_land_cessnum'),
    re_path(r'lewis_and_clark.html', lewis_and_clark, name='lewis_and_clark'),
    re_path(r'^language_learning.html$', language_learning, name='language_learning'),
    
    re_path(r'spanish/([a-z0-9_]{5,30})_([0-9]{1,3}).html', spanish_page, name='spanish_page'),
    re_path(r'spanish_main.html/', spanish_main, name='spanish_main'),
    re_path(r'ingles/([a-z0-9_]{5,40})_([0-9]{1,3}).html', ingles_page, name='ingles_page'),
    re_path(r'ingles_main.html/', ingles_main, name='ingles_main'),
    re_path(r'latin/([a-z0-9_]{5,40})_([0-9]{1,3}).html', latin_page, name='latin_page'),
    re_path(r'latin_main.html/', latin_main, name='latin_main'),
    re_path(r'verb_game/([a-z]{3,40}).html', verb_game, name='verb_game'),
    re_path(r'verb_game_main.html/', verb_game_main, name='verb_game_main'),

    re_path(r'^pic_form/$', PicFormView.as_view(), name='pic_form'),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)