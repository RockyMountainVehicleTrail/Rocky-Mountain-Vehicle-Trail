# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 14:00:33 2021

@author: mark
"""

from django.shortcuts import render

from blog.models import (LanguagePage, LanguagePageLine, SpanishWord, 
                         SpanishMorph, SpanishEngWord)
verb_list = ['viajar', 'haber', 'ser', 'estar', 'tener', 'poder', 'decir',
                 'comer', 'vivir', 'hablar', 'tener', 'hacer', 'poner',
                 'ver']


def verb_game_main(request):
  
    context = {
            'verb_list':verb_list,        
        }
        
    return render(request, 'verb_game_main.html', context)


def verb_game(request, verb):
    word = SpanishWord.objects.get(word=verb)
    morphs = SpanishMorph.objects.filter(def_id=word)
    print(morphs.count())
    count = 1
    morph_dict = {}
    for morph in morphs:
        if morph.tense:
            if len(morph.tense) > 4:
                if (morph.mood == 'subjunctive') and (morph.extra == 'se'):
                    print('sub')
                    cc = morph.tense[0:4] + morph.mood[0] + 's' + morph.person[0] + morph.number[0]
                else:
                    cc = morph.tense[0:4] + morph.mood[0] + 'a' + morph.person[0] + morph.number[0]
                morph_dict[cc]  = morph.lower_form
                count += 1
            
    print(len(morph_dict))
    print(morph_dict)
    context = {
       'word':word,
       'morph_dict':morph_dict,
       'verb_list':verb_list,   
        }
    return render(request, 'verb_game.html', context)











