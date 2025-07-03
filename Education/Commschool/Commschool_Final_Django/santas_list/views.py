from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .forms import SantasListForm, KidForm
from .models import Santas_list,Kid


# Create your views here.

def create_list(request):
    if Santas_list.objects.exists():
        # If an instance already exists, show a message and prevent further form submission
        return HttpResponse("Santa's list already exists", status=400)
    if request.method == 'GET':
        form = SantasListForm()
        return render(request, 'create_list.html', {'form': form})
    elif request.method == 'POST':
        form = SantasListForm(request.POST)
        if form.is_valid():
            form.save()
            #update kids created before santa's list was created
            kids_without_santa = Kid.objects.filter(santas_list__isnull=True)
            kids_without_santa.update(santas_list=form)
            return render(request, 'create_list.html', {'form': form})
        return HttpResponse(status=400, content="bad request")
    else:
        return HttpResponse(status=400, content="bad request")



def view_nice(request):
    santas_list = Santas_list.objects.first()

    if not santas_list:
        return HttpResponse("No Santa's list found.", status=404)

    nice_kids = santas_list.nice_list

    return render(request, 'nice_list.html', {'nice_kids': nice_kids})



def view_naughty(request):
    santas_list = Santas_list.objects.first()

    if not santas_list:
        return HttpResponse("No Santa's list found.", status=404)

    naughty_kids = santas_list.naughty_list

    return render(request, 'naughty_list.html', {'naughty_kids': naughty_kids})



def view_all_kids(request):
    santas_list = Santas_list.objects.first()

    if not santas_list:
        return HttpResponse("No Santa's list found.", status=404)

    all_kids = santas_list.get_all_kids

    return render(request, 'all_kids.html', {'all_kids': all_kids})

def remove_kid(request, kid_id):
    kid = get_object_or_404(Kid, id=kid_id)

    if kid.santas_list is not None:
        kid.santas_list = None
        kid.save()

        return JsonResponse({"message": f"Kid {kid.name} removed from Santa's list."}, status=200)
    else:
        return JsonResponse({"message": f"Kid {kid.name} is not associated with any Santa's list."}, status=400)

def create_kid(request):
    if request.method == 'GET':
        form = KidForm()
        return render(request, 'create_kid.html', {'form': form})
    elif request.method == 'POST':
        form = KidForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'create_kid.html', {'form': form})

def view_kid(request, kid_id):
    kid = get_object_or_404(Kid, id=kid_id)

    return render(request, 'view_kid.html', {'kid': kid})

