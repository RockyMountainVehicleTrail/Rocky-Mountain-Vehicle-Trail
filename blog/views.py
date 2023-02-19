from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from .models import Picture, Post, Trail
from django.contrib.gis.measure import D, Distance


   
def pview(request, pk_id):
    pic = Picture.objects.get(pk=pk_id)
    
    context = {
        'pic':pic,        
        }

    return render(request, 'pic.html', context)
    
def pview_all(request):
    pics = Picture.objects.all()
    
    context = {
        'pics':pics,        
        }

    return render(request, 'pic2.html', context)
    
def trails(request):
    trail = Trail.objects.filter(pk=1)
    trails = Trail.objects.all()[0:7]
    trails = Trail.objects.all()
    
    context = {
        'trails':trails, 
        }

    return render(request, 'trails_poly.html', context)
    
    
    
def trail_with_graph(request):
    trail = Trail.objects.get(pk=152)
    
    print(trail)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=5)))
    print(pics)
    
    context = {
        'trail': trail, 
        'pics': pics,
        }

    return render(request, 'trail_with_graph.html', context)

def trail_with_graph_2(request, pk):
    trail = Trail.objects.get(pk=pk)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=5)))
#    print(pics)
    
    print(trail)
    context = {
        'trail':trail,
        'pics': pics
        }

    return render(request, 'trail_with_graph_2.html', context)
    
def trail_with_graph_3(request, pk):
    trail = Trail.objects.get(pk=pk)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=5)))
#    print(pics)
    
    print(trail)
    context = {
        'trail':trail,
        'pics': pics
        }

    return render(request, 'trail_with_graph_3.html', context)
    

def trail_with_bargraph_1(request, pk):
    trail = Trail.objects.get(pk=pk)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=5)))
#    print(pics)
    
    print(trail)
    context = {
        'trail':trail,
        'pics': pics
        }

    return render(request, 'trail_with_bargraph_1.html', context)




def trail_with_pics(request, pk):
    trail = Trail.objects.get(pk=pk)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=5)))
    pic_list = []
    cpic = 0
    
    num_pics = pics.count() - 1
    while (cpic < num_pics):
        print('{} c:{}'.format(num_pics, cpic))
        iloop = 0
        ilist = []
        while (cpic < num_pics) and (iloop < 3):
            ilist.append(pics[cpic])
            cpic = cpic + 1
            iloop = iloop + 1
        pic_list.append(ilist)
#    num_pics = 21    
#    while (cpic < num_pics):
#        print('{} c:{}'.format(num_pics, cpic))
#        iloop = 0
#        ilist = []
#        while (cpic < num_pics) and (iloop < 3):
#            ilist.append(cpic)
#            cpic = cpic + 1
#            iloop = iloop + 1
#        pic_list.append(ilist)

    
    print(trail)
    context = {
        'trail':trail,
        'pics': pics,
        'pic_list': pic_list,
        }

    return render(request, 'trail_with_pics.html', context)
    
def trail_with_pics_2(request, pk):
    trail = Trail.objects.get(pk=pk)
    lstr = trail.line_string
    pics = Picture.objects.filter(point__distance_lt=(lstr, D(m=100)))
    pic_list = []
    cpic = 0
    



    
    print(trail)
    context = {
        'trail':trail,
        'pics': pics,
 
        }

    return render(request, 'trail_with_pics_2.html', context)













