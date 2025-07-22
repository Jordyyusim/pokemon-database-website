from django.shortcuts import render
from django.http import HttpResponse
from .utils.app import main

def index(request):
    return render(request, 'index.html')

# def results(request):
#     pokemon = request.GET.get('poke')
#     result = main(pokemon)
#     if result:
#         return render(request, 'result.html', context={'data':result})
#     else:
#         return render(request, 'result.html', context={'eror':"Pokemon is not found"})
    
def results(request):
    pokemon = request.GET.get('poke') # samakan dengan class name .input
    data, before_after, previous_img, evolution_img = main(pokemon)
    if data:
        return render(request, 'result.html', context={'data':data,  
                                                       'id_before_after': before_after,
                                                       'prev_img':previous_img,
                                                       'evo_img':evolution_img})
    else:
        return render(request, 'result.html', context={'eror':"Pokemon is not found"})