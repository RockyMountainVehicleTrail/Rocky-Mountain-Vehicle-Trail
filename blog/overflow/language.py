from django.shortcuts import render
from django.db.models import Q

from blog.models import (LanguagePage, LanguagePageLine, SpanishWord, 
                         SpanishMorph, SpanishEngWord)
import string, json
import nltk.stem.wordnet



def spanish_main(request):
    pages = LanguagePage.objects.filter(language='spanish')
    context = {
        'pages':pages    
    }
    return render(request, 'spanish_main.html', context)
    
    
def ingles_main(request):
    pages = LanguagePage.objects.filter(language='ingles')
    context = {    
        'pages':pages    
    }
    return render(request, 'ingles_main.html', context)
    
def make_json_spanish_english(lines):
    
    """
    creates a JSON dictionary for use in the website with the spanish to english
    word bindings.
    """
    punc = string.punctuation + '¡' + '¿' +'¡'
    spanish_word_set = set()
    for line in lines:
        for word in line.spanish.replace('-',' ').split(' '):
            strip_word = word
            for c in punc:
                strip_word = strip_word.replace(c, '')
            if len(strip_word) > 0:
                spanish_word_set.add(strip_word.lower())
    
    new_results = {}      
    not_found_set = set()
    for outer_word in spanish_word_set:
#        if outer_word.lower()[-2:] == 'me':
        # take care of reflexive verbs etc.
        morphs = SpanishMorph.objects.filter(
            Q( lower_form=outer_word.lower()) | 
            Q(lower_form=outer_word.lower()[:-2]) | 
            Q(lower_form=outer_word.lower()[:-3])
            )

        if morphs.count() == 0:
            not_found_set.add(outer_word)
        def_set = set([morph.def_id for morph in morphs])
        def_list = list(def_set)
        sub_result = []
        for word in def_list:
#            print('word_for: {} {}'.format(word, word.word))
            user_json = {}
            user_json['word'] = []
            user_json['word'].append('{} -{} : {}'.format(word.word,
                                                        word.pos,
                                                        word.eng_trans))
            user_json['full_def'] = word.eng_trans
            user_json['morphs'] = []
            for morph in morphs.filter(def_id=word):
#                print(morph, morph.concat)
                user_json['morphs'].append(morph.concat)
            sub_result.append(user_json)
        new_results[outer_word] = sub_result        
    
    # Make eng_version
    
    english_word_set = set()
    english_lemma_set = set()
    for line in lines:
        if line.english:
            for word in line.english.replace('-',' ').split(' '):
                strip_word = word
                for c in punc:
                    strip_word = strip_word.replace(c, '')
                if len(strip_word) > 0:
                    english_word_set.add(strip_word.lower())
    print('eng_word_set {}'.format(english_word_set))
    
    wl = nltk.stem.wordnet.WordNetLemmatizer()
    pos_list = ['a', 'n', 'r', 's', 'v']
    
    for outer_word in english_word_set:
        english_lemma_set = set()
        for pos_char in pos_list:
            print('Outer word {}\tpos {}'.format(outer_word, pos_char))
            # try and find the root word in English it is harder to make a 
            # morphological table than say Latin or Spanish
            english_lemma_set.add(wl.lemmatize(outer_word, pos=pos_char))
    
        for lemma_word in english_lemma_set:
            eng_words_found = SpanishEngWord.objects.filter(word=lemma_word)
            print('for loop lemmaword {} - {}'.format(lemma_word, eng_words_found.count()))
            if eng_words_found.count() >= 1:
                sub_result = []
                for found_word in eng_words_found:
                    user_json = {}
                    user_json['word'] = []
                    user_json['word'].append('{} {} - {}'.format(found_word.word,
                                                                 found_word.pos, 
                                                                 found_word.spanish_phrase))
                    user_json['full_def'] = found_word.spanish_phrase
                    user_json['lang'] = 'english'
                    user_json['morphs'] = []
                    sub_result.append(user_json)
                                            
                    new_results[outer_word] = sub_result

    json_dict = json.dumps(new_results, ensure_ascii=False)
    return json_dict

	
def spanish_page(request, lang_page_title, chapter_num):

#    print(book_name, chapter_num)
    punc = string.punctuation + '¡' + '¿' +'¡'
    
    lpage = LanguagePage.objects.get(url_title=lang_page_title)
    all_parts = LanguagePageLine.objects.filter(language_page=lpage)
    parts = all_parts.distinct('chapter')
    
    lines = LanguagePageLine.objects.filter(language_page=lpage).filter(chapter=str(chapter_num)).order_by('line_num')

    json_dict = make_json_spanish_english(lines)
            
    context = {
            'language_page': lpage,
            'lines':lines,
            'json_dict':json_dict,
            'parts':parts,
        }
            
    return render(request, 'spanish_page.html', context)

    
def ingles_page(request, lang_page_title, chapter_num):

    # punc = string.punctuation + '¡' + '¿' +'¡'
    
    lpage = LanguagePage.objects.get(url_title=lang_page_title)
    all_parts = LanguagePageLine.objects.filter(language_page=lpage)
    parts = all_parts.distinct('chapter')
    
    lines = LanguagePageLine.objects.filter(language_page=lpage).filter(chapter=str(chapter_num)).order_by('line_num')
        
    json_dict = make_json_spanish_english(lines)
            
    context = {
            'language_page': lpage,
            'lines':lines,
            'json_dict':json_dict,
            'parts':parts,
        }
            
           
    return render(request, 'ingles_page.html', context)

   