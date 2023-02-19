from django.shortcuts import render

from blog.models import (LanguagePage, LanguagePageLine, WhitFull, WhitMorphFull)
import string, json


def latin_main(request):
    pages = LanguagePage.objects.filter(language='latin')

    context = {
        'pages':pages    
    }

    return render(request, 'latin_main.html', context)



def make_json(lines):
    """
    Make a json dictionary of all words forms and etc for an offline dictionary
    for viewing on phones and what not
    """
    
    punc = string.punctuation + '¡' + '¿' +'¡'
    # Find all words for all lines that will be passed to the template
    latin_word_set = set([])
    for line in lines:
        for word in line.latin.replace('-',' ').split(' '):
            strip_word = word
            for c in punc:
                strip_word = strip_word.replace(c, '')
            if len(strip_word) > 0:
                latin_word_set.add(strip_word.lower())

    new_results = {}

    for outer_word in latin_word_set:
        # there is some error when creating the database that requires this line
        if outer_word == 'erat':
            pass
        else:
#            print(outer_word)
            morphs = WhitMorphFull.objects.filter(lower_form=outer_word.lower())
            # que like filoque "and the son" is common in latin but can be removed
            # to find the underlying word
            if (morphs.count() == 0) and (outer_word.lower()[-3:] == 'que'):
                morphs = WhitMorphFull.objects.filter(lower_form=outer_word.lower()[:-3])
            if morphs.count() > 40:
                print('Too many morphs', outer_word)
            else:
                # removed duplicates but put back in order
                def_set = set([morph.def_id for morph in morphs])
                def_list = list(def_set)
                sub_result = []
                # went back and forth with the json format and displaying on web page
                for word in def_list:
                    user_json = {}
                    user_json['word'] = []
                    user_json['word'].append('{} -{}-{} : {}'.format(word.word,
                                                                word.pos,
                                                                word.pos_group,
                                                                word.definition[0:50]))
                    user_json['full_def'] = word.definition
                    user_json['morphs'] = []
                    for morph in morphs.filter(def_id=word):
                        user_json['morphs'].append(morph.concat + ' ' + morph.verb_sub)
                    sub_result.append(user_json)
                new_results[outer_word] = sub_result

    return new_results
	
 
def latin_page(request, lang_page_title, chapter_num):
    
    lpage = LanguagePage.objects.get(url_title=lang_page_title)
    all_parts = LanguagePageLine.objects.filter(language_page=lpage)
    parts = all_parts.distinct('chapter')
    
    lines = LanguagePageLine.objects.filter(language_page=lpage).filter(chapter=str(chapter_num)).order_by('line_num')        
    
    morph_def_dict = make_json(lines)
    json_dict = json.dumps(morph_def_dict, ensure_ascii=False)
                
    context = {
            'lines':lines,
            'json_dict':json_dict,
            'parts':parts,
        }
            

    return render(request, 'latin_page.html', context)
